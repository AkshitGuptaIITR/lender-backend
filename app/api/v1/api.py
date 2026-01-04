from fastapi import APIRouter
from app.api.v1.endpoints import health, lender, lender_policy, business

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(lender.router, prefix="/lender", tags=["lender"])
api_router.include_router(
    lender_policy.router, prefix="/lender-policy", tags=["lender_policy"]
)
api_router.include_router(business.router, prefix="/business", tags=["business"])
