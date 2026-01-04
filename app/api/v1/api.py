from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    lender,
    lender_policy,
    business,
    personal_guarantor,
    matching_engine,
)

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(lender.router, prefix="/lender", tags=["lender"])
api_router.include_router(
    lender_policy.router, prefix="/lender-policy", tags=["lender_policy"]
)
api_router.include_router(business.router, prefix="/business", tags=["business"])
api_router.include_router(
    personal_guarantor.router, prefix="/personal-guarantor", tags=["personal_guarantor"]
)
api_router.include_router(
    matching_engine.router, prefix="/matching-engine", tags=["matching_engine"]
)
