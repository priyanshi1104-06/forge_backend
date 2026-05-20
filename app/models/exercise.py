from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id         = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("workout_sessions.id"))
    name       = Column(String, nullable=False)
    sets       = Column(Integer, nullable=False)
    reps       = Column(Integer, nullable=False)
    weight_kg  = Column(Float, nullable=False)

    session = relationship("WorkoutSession", back_populates="exercises")