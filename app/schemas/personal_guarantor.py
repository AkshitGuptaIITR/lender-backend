from pydantic import BaseModel


class PersonalGuarantorCreate(BaseModel):
    fico_score: int
    trade_lines: int
    credit_history_flags: str
    lender_policy_id: int


class PersonalGuarantorResponse(BaseModel):
    id: int
    fico_score: int
    trade_lines: int
    credit_history_flags: str
    lender_policy_id: int
