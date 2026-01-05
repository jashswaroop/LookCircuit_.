"""
Recommendations API Endpoints
Provides personalized style and color recommendations.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel

from app.api import deps
from app.schemas.user import User

# Import recommendation engine (with fallback for path issues)
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ai.recommendation_engine.color_theory import RecommendationEngine
from ai.recommendation_engine.occasion_styling import OccasionStylingEngine

router = APIRouter()

# Initialize engines
_recommendation_engine = None
_occasion_engine = None

def get_recommendation_engine() -> RecommendationEngine:
    global _recommendation_engine
    if _recommendation_engine is None:
        _recommendation_engine = RecommendationEngine()
    return _recommendation_engine

def get_occasion_engine() -> OccasionStylingEngine:
    global _occasion_engine
    if _occasion_engine is None:
        _occasion_engine = OccasionStylingEngine()
    return _occasion_engine


class RecommendationRequest(BaseModel):
    """Request model for generating recommendations."""
    fitzpatrick_type: int
    undertone: str
    face_shape: str
    body_type: str = "mesomorph"
    hair_coverage: str = "full"
    gender: str = "male"


@router.post("/generate")
async def generate_recommendations(
    request: RecommendationRequest,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Generate personalized style recommendations based on analysis results.
    
    Returns:
    - Color palette (season, best colors, avoid colors)
    - Style recommendations (necklines, patterns, fits)
    - Grooming recommendations (hairstyles, beard styles)
    - Reasoning for each recommendation
    """
    try:
        engine = get_recommendation_engine()
        recommendations = engine.generate_recommendations(
            fitzpatrick_type=request.fitzpatrick_type,
            undertone=request.undertone,
            face_shape=request.face_shape,
            body_type=request.body_type,
            hair_coverage=request.hair_coverage,
            gender=request.gender
        )
        
        return JSONResponse(content={
            "success": True,
            "recommendations": recommendations
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation generation failed: {str(e)}")


@router.get("/occasion/{occasion}")
async def get_occasion_outfit(
    occasion: str,
    gender: str = Query(default="male"),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get outfit recommendations for a specific occasion.
    
    Supported occasions: casual, formal, business_casual, date_night, fitness, festive, interview
    """
    try:
        engine = get_occasion_engine()
        
        # Default color palette if not provided
        default_palette = ["#000080", "#FFFFFF", "#808080", "#8B4513"]
        
        outfit = engine.get_occasion_outfit(
            occasion=occasion,
            gender=gender,
            color_palette=default_palette,
            face_shape="oval"
        )
        
        return JSONResponse(content={
            "success": True,
            "outfit": {
                "occasion": outfit.occasion,
                "top": outfit.top,
                "bottom": outfit.bottom,
                "footwear": outfit.footwear,
                "accessories": outfit.accessories,
                "grooming_notes": outfit.grooming_notes,
                "color_suggestions": outfit.color_suggestions
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Outfit generation failed: {str(e)}")


@router.get("/occasions")
async def list_occasions(
    current_user: User = Depends(deps.get_current_user)
):
    """List all available occasion types."""
    engine = get_occasion_engine()
    return JSONResponse(content={
        "occasions": engine.get_all_occasions()
    })


@router.get("/health")
async def recommendations_health():
    """Check if recommendation service is ready."""
    try:
        engine = get_recommendation_engine()
        return {"status": "ready", "engine": "initialized"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
