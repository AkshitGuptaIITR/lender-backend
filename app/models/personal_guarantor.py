from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.models.base import Base


class PersonalGuarantor(Base):
    __tablename__ = "personal_guarantor"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    fico_score = Column(Integer, nullable=False)
    trade_lines = Column(Integer, nullable=False)
    credit_history_flags = Column(String, nullable=False)
    lender_policy_id = Column(
        Integer,
        ForeignKey("lender_policy.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lender_policy = relationship("LenderPolicy", back_populates="personal_guarantors")
