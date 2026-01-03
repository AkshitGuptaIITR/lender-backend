from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.lender import Lender
from app.schemas.response import APIResponse
from app.schemas.lender import LenderCreate, LenderResponse
from sqlalchemy import select

router = APIRouter()


@router.post("/", response_model=APIResponse[LenderResponse])
async def create_lender(
    lender_in: LenderCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        # Test database connection
        lender = Lender(name=lender_in.name)
        db.add(lender)
        await db.commit()
        await db.refresh(lender)
        return APIResponse(data=lender)
    except Exception as e:
        return APIResponse(status="error", message=str(e))


@router.get("/", response_model=APIResponse[list[LenderResponse]])
async def get_lenders(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Lender))
        lenders = result.scalars().all()
        return APIResponse(data=lenders)
    except Exception as e:
        return APIResponse(status="error", message=str(e))


@router.get("/{lender_id}", response_model=APIResponse[LenderResponse])
async def get_lender(lender_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Lender).where(Lender.id == lender_id))
        lender = result.scalar_one_or_none()
        if not lender:
            return APIResponse(status="error", message="Lender not found")
        return APIResponse(data=lender)
    except Exception as e:
        return APIResponse(status="error", message=str(e))
