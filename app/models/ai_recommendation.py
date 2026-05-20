from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"))
    type         = Column(String, nullable=False)
    content      = Column(String, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active    = Column(Boolean, default=True)