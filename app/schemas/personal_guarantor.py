from pydantic import BaseModel


class PersonalGuarantorCreate(BaseModel):
    fico_score: int
    trade_lines: int
    credit_history_flags: str
    name: str


class PersonalGuarantorResponse(BaseModel):
    id: int
    fico_score: int
    trade_lines: int
    credit_history_flags: str
    name: str
