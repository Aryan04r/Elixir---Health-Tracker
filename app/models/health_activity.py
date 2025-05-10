from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.base import Base

class ActivityType(enum.Enum):
    FITNESS = "fitness"
    CHECKIN = "checkin"

class HealthActivity(Base):
    __tablename__ = "health_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_type = Column(Enum(ActivityType))
    points_earned = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # For fitness activities
    activity_name = Column(String, nullable=True)  # e.g., "steps", "workout", "yoga"
    activity_value = Column(Float, nullable=True)  # e.g., number of steps, workout duration
    
    # For daily check-in
    mood_score = Column(Integer, nullable=True)  # 1-10
    sleep_hours = Column(Float, nullable=True)
    water_intake = Column(Float, nullable=True)  # in liters
    
    # Relationship with User
    user = relationship("User", back_populates="health_activities") 