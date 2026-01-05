"""
Products API Endpoints
Provides product discovery and search functionality.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel

from app.api import deps
from app.schemas.user import User

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ai.product_discovery.scraper import ProductDiscoveryEngine

router = APIRouter()

# Initialize engine
_discovery_engine = None

def get_discovery_engine() -> ProductDiscoveryEngine:
    global _discovery_engine
    if _discovery_engine is None:
        _discovery_engine = ProductDiscoveryEngine()
    return _discovery_engine


class ProductSearchRequest(BaseModel):
    """Request for product search."""
    color_palette: List[str]
    categories: List[str]
    occasion: Optional[str] = None
    max_results: int = 20


@router.post("/discover")
async def discover_products(
    request: ProductSearchRequest,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Discover products matching user's style profile.
    
    Args:
        color_palette: Recommended colors from analysis
        categories: Product categories to search
        occasion: Optional occasion filter
        
    Returns:
        Products organized by category
    """
    try:
        engine = get_discovery_engine()
        products = engine.discover_products(
            color_palette=request.color_palette,
            categories=request.categories,
            occasion=request.occasion,
            max_results=request.max_results
        )
        
        return JSONResponse(content={
            "success": True,
            "products": products,
            "total_count": sum(len(p) for p in products.values())
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Product discovery failed: {str(e)}")


@router.get("/categories")
async def get_categories(
    current_user: User = Depends(deps.get_current_user)
):
    """List all available product categories."""
    from ai.product_discovery.scraper import ProductCategory
    return JSONResponse(content={
        "categories": [c.value for c in ProductCategory]
    })


@router.get("/health")
async def products_health():
    """Check if product service is ready."""
    try:
        engine = get_discovery_engine()
        return {"status": "ready", "engine": "initialized"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
