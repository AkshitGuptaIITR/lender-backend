from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.business import Business
from app.schemas.response import APIResponse
from app.schemas.business import BusinessCreate, BusinessResponse
from sqlalchemy import select
from app.models.lender_policy import LenderPolicy
from fastapi import HTTPException

router = APIRouter()


@router.post("/", response_model=APIResponse[BusinessResponse])
async def create_business(
    business_in: BusinessCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        business = Business(
            name=business_in.name,
            geographic_location=business_in.geographic_location,
            industry_type=business_in.industry_type,
            revenue=business_in.revenue,
            equipment_type=business_in.equipment_type,
            business_duration=business_in.business_duration,
            paynet_score=business_in.paynet_score,
        )
        db.add(business)
        await db.commit()
        await db.refresh(business)
        return APIResponse(data=business)

        db.add(business)
        await db.commit()
        await db.refresh(business)
        return APIResponse(data=business)
    except Exception as e:
        return APIResponse(status="error", message=str(e))


@router.get("/", response_model=APIResponse[list[BusinessResponse]])
async def get_businesses(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Business))
        businesses = result.scalars().all()
        return APIResponse(data=businesses)
    except Exception as e:
        return APIResponse(status="error", message=str(e))


@router.get("/{business_id}", response_model=APIResponse[BusinessResponse])
async def get_business(business_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Business).where(Business.id == business_id))
        business = result.scalar_one_or_none()
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")
        return APIResponse(data=business)
    except Exception as e:
        return APIResponse(status="error", message=str(e))
