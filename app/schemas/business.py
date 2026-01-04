from pydantic import BaseModel


class BusinessCreate(BaseModel):
    name: str
    geographic_location: str
    industry_type: str
    revenue: float
    equipment_type: str
    business_duration: int
    paynet_score: int
    lender_policy_id: int


class BusinessResponse(BaseModel):
    id: int
    name: str
    geographic_location: str
    industry_type: str
    revenue: float
    equipment_type: str
    business_duration: int
    paynet_score: int
    lender_policy_id: int
