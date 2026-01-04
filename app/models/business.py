from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.models.base import Base


class Business(Base):
    __tablename__ = "business"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    geographic_location = Column(String, nullable=False)
    industry_type = Column(String, nullable=False)
    revenue = Column(Float, nullable=False)
    equipment_type = Column(String, nullable=False)
    business_duration = Column(Integer, nullable=False)
    paynet_score = Column(Integer, nullable=False)
    lender_policy_id = Column(
        Integer,
        ForeignKey("lender_policy.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lender_policy = relationship("LenderPolicy", back_populates="businesses")
