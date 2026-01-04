from pydantic import BaseModel
from typing import Optional
from app.schemas.policy_rule import PolicyRuleResponse


class LenderPolicyBase(BaseModel):
    name: str
    lender_id: int


class LenderPolicyCreate(LenderPolicyBase):
    pass


class LenderPolicyResponse(LenderPolicyBase):
    id: int
    file_path: str
    policy_rules: list[PolicyRuleResponse] = []

    class Config:
        from_attributes = True
