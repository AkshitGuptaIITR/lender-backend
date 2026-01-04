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
    matching_engines = relationship(
        "MatchingEngine",
        back_populates="personal_guarantor",
        cascade="all, delete-orphan",
    )
