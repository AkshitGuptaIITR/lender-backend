from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.lender import Lender
from app.schemas.response import APIResponse
from app.schemas.lender import LenderCreate, LenderResponse

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
