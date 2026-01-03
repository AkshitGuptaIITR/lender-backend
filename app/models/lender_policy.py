from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.lender import Lender


class LenderPolicy(Base):
    __tablename__ = "lender_policy"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    lender_id = Column(
        Integer,
        ForeignKey("lender.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lender = relationship("Lender", back_populates="policies")
    policy_rules = relationship(
        "PolicyRule", back_populates="lender_policy", cascade="all, delete-orphan"
    )
