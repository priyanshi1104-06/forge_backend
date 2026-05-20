from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class PersonalRecord(Base):
    __tablename__ = "personal_records"

    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, ForeignKey("users.id"))
    exercise_name = Column(String, nullable=False)
    max_weight_kg = Column(Float, nullable=False)
    achieved_at   = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="records")