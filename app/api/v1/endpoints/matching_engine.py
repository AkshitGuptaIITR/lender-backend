from fastapi import APIRouter, HTTPException
from app.schemas.response import APIResponse
from app.schemas.matching_engine import MatchingEngineCreate, MatchingEngineResponse
from app.models.policy_rule import RequirementType, Operator
from app.models.matching_engine import YesNoEnum
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.matching_engine import MatchingEngine, LenderPolicy
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.schemas.lender_policy import LenderPolicyResponse
from app.models.business import Business
from app.models.personal_guarantor import PersonalGuarantor

router = APIRouter()


@router.post("/", response_model=APIResponse[list[MatchingEngineResponse]])
async def create_matching_engine(
    matching_engine_in: MatchingEngineCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        stmt = (
            select(LenderPolicy)
            .where(LenderPolicy.policy_rules.any())  # Only get policies that HAVE rules
            .options(selectinload(LenderPolicy.policy_rules))
        )
        lender_policies = await db.execute(stmt)
        lender_policies = lender_policies.scalars().all()

        if len(lender_policies) == 0:
            raise HTTPException(status_code=404, detail="Lender policies not found")

        business = Business(
            name=matching_engine_in.business_name,
            geographic_location=matching_engine_in.geographic_location,
            industry_type=matching_engine_in.industry_type,
            revenue=matching_engine_in.revenue,
            equipment_type=matching_engine_in.equipment_type,
            business_duration=matching_engine_in.business_duration,
            paynet_score=matching_engine_in.paynet_score,
        )
        db.add(business)
        await db.flush()
        await db.refresh(business)

        personal_guarantor = PersonalGuarantor(
            name=matching_engine_in.personal_guarantor_name,
            fico_score=matching_engine_in.fico_score,
            trade_lines=matching_engine_in.trade_lines,
            credit_history_flags=matching_engine_in.credit_history_flags,
        )
        db.add(personal_guarantor)
        await db.flush()
        await db.refresh(personal_guarantor)

        response = []

        for lender_policy in lender_policies:
            eligibility = YesNoEnum.YES
            matching_tier = None
            rejection_reason = []
            fit_score = 0
            loan_amount = matching_engine_in.loan_amount
            lender_policy_id = lender_policy.id

            total_points_earned = 0
            possible_points = 0
            weights = {
                "fico_score": 50,
                "business_duration": 30,
                "paynet_score": 20,
                "default": 10,
            }

            for policy_rule in lender_policy.policy_rules:
                value = policy_rule.field_value
                field_name = policy_rule.field_name
                operator = policy_rule.operator
                requirement_type = policy_rule.requirement_type
                error_message = policy_rule.error_message
                is_matching = True

                if field_name == "other":
                    continue

                input_value = getattr(matching_engine_in, field_name, None)
                if input_value is None:
                    print(field_name, "Not there")
                    is_matching = False

                try:
                    if isinstance(input_value, int):
                        value = int(value)
                    elif isinstance(input_value, float):
                        value = float(value)
                    elif isinstance(input_value, bool):
                        value = value.lower() in ["true", "1", "yes"]
                except:
                    continue

                if not is_matching:
                    if requirement_type == RequirementType.HARD_STOP:
                        print(field_name, value, input_value)
                        eligibility = YesNoEnum.NO
                    continue

                if operator == Operator.EQUAL:
                    if input_value != value:
                        rejection_reason.append(error_message)
                        is_matching = False
                elif operator == Operator.NOT_EQUAL:
                    if input_value == value:
                        rejection_reason.append(error_message)
                        is_matching = False
                elif operator == Operator.GREATER_THAN:
                    if input_value <= value:
                        rejection_reason.append(error_message)
                        is_matching = False
                elif operator == Operator.LESS_THAN:
                    if input_value >= value:
                        rejection_reason.append(error_message)
                        is_matching = False
                elif operator == Operator.GREATER_THAN_OR_EQUAL:
                    if input_value < value:
                        rejection_reason.append(error_message)
                        is_matching = False
                elif operator == Operator.LESS_THAN_OR_EQUAL:
                    if input_value > value:
                        rejection_reason.append(error_message)
                        is_matching = False
                elif operator == Operator.NOT_IN:
                    # For string checks, IN/NOT_IN usually implies value is a list or substring check
                    if str(input_value) in str(value):
                        rejection_reason.append(error_message)
                        is_matching = False
                elif operator == Operator.IN:
                    if str(input_value) not in str(value):
                        rejection_reason.append(error_message)
                        is_matching = False
                elif operator == Operator.LIKE:
                    if str(input_value) not in str(value):
                        rejection_reason.append(error_message)
                        is_matching = False
                elif operator == Operator.NOT_LIKE:
                    if str(input_value) in str(value):
                        rejection_reason.append(error_message)
                        is_matching = False
                elif operator == Operator.IS:
                    if input_value != value:
                        rejection_reason.append(error_message)
                        is_matching = False
                elif operator == Operator.IS_NOT:
                    if input_value == value:
                        rejection_reason.append(error_message)
                        is_matching = False
                elif operator == Operator.CONTAINS:
                    if str(value) not in str(input_value):
                        rejection_reason.append(error_message)
                        is_matching = False
                elif operator == Operator.NOT_CONTAINS:
                    if str(value) in str(input_value):
                        rejection_reason.append(error_message)
                        is_matching = False

                rule_weight = weights.get(field_name, weights["default"])

                if not is_matching:
                    if requirement_type == RequirementType.HARD_STOP:
                        print(field_name, value, input_value)
                        eligibility = YesNoEnum.NO
                else:
                    # If it matches and it's a soft match, add to score
                    if requirement_type == RequirementType.SOFT_MATCH:
                        total_points_earned += rule_weight

                if requirement_type == RequirementType.SOFT_MATCH:
                    possible_points += rule_weight

            if eligibility == YesNoEnum.NO:
                fit_score = 0
            elif possible_points == 0:
                fit_score = 100
            else:
                fit_score = round((total_points_earned / possible_points) * 100)
            matching_engine = MatchingEngine(
                eligibility=eligibility,
                matching_tier=matching_tier,
                rejection_reason=(
                    ", ".join(rejection_reason) if len(rejection_reason) > 0 else None
                ),
                fit_score=fit_score,
                loan_amount=loan_amount,
                lender_policy_id=lender_policy_id,
                business_id=business.id,
                personal_guarantor_id=personal_guarantor.id,
            )

            db.add(matching_engine)
            await db.flush()
            await db.refresh(matching_engine)

            response.append(
                MatchingEngineResponse(
                    id=matching_engine.id,
                    business_name=matching_engine_in.business_name,
                    personal_guarantor_name=matching_engine_in.personal_guarantor_name,
                    eligibility=eligibility,
                    matching_tier=matching_tier,
                    rejection_reason=(
                        ", ".join(rejection_reason)
                        if len(rejection_reason) > 0
                        else None
                    ),
                    fit_score=fit_score,
                    loan_amount=loan_amount,
                    lender_policy_id=lender_policy_id,
                    business_id=business.id,
                    personal_guarantor_id=personal_guarantor.id,
                )
            )

        await db.commit()
        return APIResponse(data=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
