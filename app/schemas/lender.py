from pydantic import BaseModel


class LenderCreate(BaseModel):
    name: str


class LenderResponse(LenderCreate):
    id: int

    class Config:
        from_attributes = True
