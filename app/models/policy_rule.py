from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.lender_policy import LenderPolicy
import enum


class Operator(str, enum.Enum):
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
    LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"
    NOT_IN = "NOT_IN"
    IN = "IN"
    LIKE = "LIKE"
    NOT_LIKE = "NOT_LIKE"
    IS = "IS"
    IS_NOT = "IS_NOT"


class PolicyRule(Base):
    __tablename__ = "policy_rule"
    id = Column(Integer, primary_key=True, index=True)
    field_name = Column(String, nullable=False)
    field_value = Column(String, nullable=False)
    operator = Column(Enum(Operator, name="operator_type"), nullable=False)
    lender_policy_id = Column(
        Integer,
        ForeignKey("lender_policy.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lender_policy = relationship("LenderPolicy", back_populates="policy_rules")
