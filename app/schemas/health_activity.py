from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.health_activity import ActivityType

class HealthActivityBase(BaseModel):
    activity_type: ActivityType

class FitnessActivityCreate(HealthActivityBase):
    activity_name: str
    activity_value: float

class DailyCheckInCreate(HealthActivityBase):
    mood_score: int
    sleep_hours: float
    water_intake: float

class HealthActivity(HealthActivityBase):
    id: int
    user_id: int
    points_earned: int
    created_at: datetime
    activity_name: Optional[str] = None
    activity_value: Optional[float] = None
    mood_score: Optional[int] = None
    sleep_hours: Optional[float] = None
    water_intake: Optional[float] = None

    class Config:
        orm_mode = True 