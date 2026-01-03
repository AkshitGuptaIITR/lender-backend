from fastapi import APIRouter
from app.api.v1.endpoints import health, lender

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(lender.router, prefix="/lender", tags=["lender"])
