from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"))
    date         = Column(Date, nullable=False)
    duration_mins = Column(Integer, nullable=True)
    notes        = Column(String, nullable=True)

    user      = relationship("User", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="session")