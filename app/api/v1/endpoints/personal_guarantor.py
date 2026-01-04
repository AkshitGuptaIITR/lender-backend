from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.personal_guarantor import PersonalGuarantor
from app.schemas.response import APIResponse
from app.schemas.personal_guarantor import (
    PersonalGuarantorCreate,
    PersonalGuarantorResponse,
)
from sqlalchemy import select
from app.models.lender_policy import LenderPolicy
from fastapi import HTTPException

router = APIRouter()


@router.post("/", response_model=APIResponse[PersonalGuarantorResponse])
async def create_personal_guarantor(
    personal_guarantor_in: PersonalGuarantorCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        personal_guarantor = PersonalGuarantor(
            fico_score=personal_guarantor_in.fico_score,
            trade_lines=personal_guarantor_in.trade_lines,
            credit_history_flags=personal_guarantor_in.credit_history_flags,
            name=personal_guarantor_in.name,
        )
        db.add(personal_guarantor)
        await db.commit()
        await db.refresh(personal_guarantor)
        return APIResponse(data=personal_guarantor)
    except Exception as e:
        return APIResponse(status="error", message=str(e))


@router.get("/", response_model=APIResponse[list[PersonalGuarantorResponse]])
async def get_personal_guarantors(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(PersonalGuarantor))
        personal_guarantors = result.scalars().all()
        return APIResponse(data=personal_guarantors)
    except Exception as e:
        return APIResponse(status="error", message=str(e))


@router.get(
    "/{personal_guarantor_id}", response_model=APIResponse[PersonalGuarantorResponse]
)
async def get_personal_guarantor(
    personal_guarantor_id: int, db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(PersonalGuarantor).where(
                PersonalGuarantor.id == personal_guarantor_id
            )
        )
        personal_guarantor = result.scalar_one_or_none()
        if not personal_guarantor:
            raise HTTPException(status_code=404, detail="Personal guarantor not found")
        return APIResponse(data=personal_guarantor)
    except Exception as e:
        return APIResponse(status="error", message=str(e))
