"""
Analysis API Endpoints
Provides endpoints for face and style analysis.
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import tempfile
import os

from app.api import deps
from app.schemas.user import User

# Import AI modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from ai.face_analysis import FaceAnalyzer

router = APIRouter()

# Initialize analyzer (singleton pattern for efficiency)
_analyzer = None

def get_analyzer() -> FaceAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = FaceAnalyzer()
    return _analyzer


@router.post("/face")
async def analyze_face(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Analyze face from uploaded image.
    
    Returns:
    - Skin tone (Fitzpatrick scale + undertone)
    - Face shape
    - Hair coverage level
    - Color season recommendation
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Could not decode image")
        
        # Validate minimum resolution
        height, width = image.shape[:2]
        if height < 480 or width < 480:
            raise HTTPException(
                status_code=400, 
                detail=f"Image resolution too low ({width}x{height}). Minimum 480x480 required."
            )
        
        # Run analysis
        analyzer = get_analyzer()
        result = analyzer.analyze(image)
        
        if not result.detected:
            raise HTTPException(status_code=400, detail="No face detected in image")
        
        return JSONResponse(content={
            "success": True,
            "analysis": result.to_dict()
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/health")
async def analysis_health():
    """Check if analysis service is ready."""
    try:
        analyzer = get_analyzer()
        return {"status": "ready", "analyzer": "initialized"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
