from pydantic import BaseModel
from typing import Optional
from app.models.matching_engine import YesNoEnum


class MatchingEngineCreate(BaseModel):
    business_name: str
    geographic_location: str
    industry_type: str
    revenue: float
    equipment_type: str
    business_duration: int
    paynet_score: int
    personal_guarantor_name: str
    fico_score: int
    trade_lines: int
    credit_history_flags: str
    loan_amount: int


class MatchingEngineResponse(BaseModel):
    id: Optional[int]
    eligibility: Optional[YesNoEnum]
    matching_tier: Optional[str]
    rejection_reason: Optional[str]
    fit_score: Optional[int]
    lender_policy_id: Optional[int]
    business_id: Optional[int]
    personal_guarantor_id: Optional[int]
