from fastapi import APIRouter
from app.schemas.response import APIResponse
from app.schemas.matching_engine import MatchingEngineCreate, MatchingEngineResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.matching_engine import MatchingEngine, LenderPolicy
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload

router = APIRouter()


from app.schemas.lender_policy import LenderPolicyResponse


@router.post("/", response_model=APIResponse[list[LenderPolicyResponse]])
async def create_matching_engine(
    matching_engine_in: MatchingEngineCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        # matching_engine = MatchingEngine(
        #     name=matching_engine_in.name,
        #     file_path=matching_engine_in.file_path,
        #     lender_id=matching_engine_in.lender_id,
        # )
        # db.add(matching_engine)
        # await db.commit()
        # await db.refresh(matching_engine)
        # return APIResponse(data=matching_engine)
        stmt = (
            select(LenderPolicy)
            .where(LenderPolicy.policy_rules.any())  # Only get policies that HAVE rules
            .options(selectinload(LenderPolicy.policy_rules))
        )
        lender_policies = await db.execute(stmt)
        lender_policies = lender_policies.scalars().all()

        if lender_policies.__len__ == 0:
            raise HTTPException(status_code=404, detail="Lender policies not found")

        return APIResponse(data=lender_policies)
    except Exception as e:
        return APIResponse(status="error", message=str(e))
