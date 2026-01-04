from pydantic import BaseModel
from typing import Optional


class LenderPolicyBase(BaseModel):
    name: str
    lender_id: int


class LenderPolicyCreate(LenderPolicyBase):
    pass


class LenderPolicyResponse(LenderPolicyBase):
    id: int
    file_path: str

    class Config:
        from_attributes = True
