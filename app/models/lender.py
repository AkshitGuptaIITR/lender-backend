from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime


class Lender(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    policies = relationship(
        "LenderPolicy", back_populates="lender", cascade="all, delete-orphan"
    )
