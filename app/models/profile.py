from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UserProfile(Base):
    __tablename__ = "profiles"

    id               = Column(Integer, primary_key=True, index=True)
    user_id          = Column(Integer, ForeignKey("users.id"), unique=True)
    age              = Column(Integer, nullable=True)
    weight_kg        = Column(Float, nullable=True)
    height_cm        = Column(Float, nullable=True)
    fitness_goal     = Column(String, nullable=True)
    experience_level = Column(String, nullable=True)

    user = relationship("User", back_populates="profile")