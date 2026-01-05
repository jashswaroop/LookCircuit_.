from fastapi import APIRouter
from app.api.v1 import users, analysis, recommendations, products

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
