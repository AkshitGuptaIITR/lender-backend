from pydantic import BaseModel


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


class MatchingEngineResponse(BaseModel):
    id: int
    eligibility: str
    matching_tier: str
    rejection_reason: str
    fit_score: int
    lender_policy_id: int
    business_id: int
    personal_guarantor_id: int
