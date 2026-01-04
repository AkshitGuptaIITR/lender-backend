from pydantic import BaseModel
from app.models.policy_rule import Operator, RequirementType
from typing import Optional


class PolicyRuleBase(BaseModel):
    field_name: str
    field_value: str
    operator: Operator
    error_message: str
    requirement_type: RequirementType
    lender_policy_id: int


class PolicyRuleCreate(PolicyRuleBase):
    pass


class PolicyRuleResponse(PolicyRuleBase):
    id: int

    class Config:
        from_attributes = True
