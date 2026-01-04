from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from app.models.base import Base
import enum
from sqlalchemy.orm import relationship
from app.models.business import Business
from app.models.personal_guarantor import PersonalGuarantor
from app.models.lender_policy import LenderPolicy


class YesNoEnum(str, enum.Enum):
    YES = "YES"
    NO = "NO"


class MatchingEngine(Base):
    __tablename__ = "matching_engine"
    id = Column(Integer, primary_key=True, index=True)
    eligibility = Column(Enum(YesNoEnum, name="yes_no_enum"), nullable=False)
    matching_tier = Column(String, nullable=True)
    rejection_reason = Column(String, nullable=True)
    fit_score = Column(Integer, nullable=True)
    lender_policy_id = Column(Integer, ForeignKey("lender_policy.id"), nullable=True)
    lender_policy = relationship("LenderPolicy", back_populates="matching_engine")
    business_id = Column(Integer, ForeignKey("business.id"), nullable=True)
    business = relationship("Business", back_populates="matching_engine")
    personal_guarantor_id = Column(
        Integer, ForeignKey("personal_guarantor.id"), nullable=True
    )
    personal_guarantor = relationship(
        "PersonalGuarantor", back_populates="matching_engine"
    )
