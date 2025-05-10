from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.health_activity import HealthActivity, ActivityType
from app.schemas.health_activity import (
    HealthActivity as HealthActivitySchema,
    FitnessActivityCreate,
    DailyCheckInCreate
)

router = APIRouter()

# Points calculation logic
def calculate_points(activity: HealthActivity) -> int:
    if activity.activity_type == ActivityType.FITNESS:
        if activity.activity_name == "steps":
            return int(activity.activity_value / 1000)  # 1 point per 1000 steps
        elif activity.activity_name == "workout":
            return int(activity.activity_value * 10)  # 10 points per hour
        elif activity.activity_name == "yoga":
            return int(activity.activity_value * 15)  # 15 points per hour
    elif activity.activity_type == ActivityType.CHECKIN:
        return 5  # 5 points for daily check-in
    return 0

@router.post("/fitness", response_model=HealthActivitySchema)
async def log_fitness_activity(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    activity: FitnessActivityCreate
):
    """
    Log a fitness activity and earn points.
    """
    health_activity = HealthActivity(
        user_id=current_user.id,
        activity_type=ActivityType.FITNESS,
        activity_name=activity.activity_name,
        activity_value=activity.activity_value
    )
    
    health_activity.points_earned = calculate_points(health_activity)
    
    db.add(health_activity)
    db.commit()
    db.refresh(health_activity)
    
    # Update user's elixir score
    current_user.elixir_score += health_activity.points_earned
    db.commit()
    
    return health_activity

@router.post("/check-in", response_model=HealthActivitySchema)
async def daily_check_in(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    check_in: DailyCheckInCreate
):
    """
    Perform daily health check-in and earn points.
    """
    # Check if user has already checked in today
    today = date.today()
    existing_check_in = db.query(HealthActivity).filter(
        HealthActivity.user_id == current_user.id,
        HealthActivity.activity_type == ActivityType.CHECKIN,
        HealthActivity.created_at >= today
    ).first()
    
    if existing_check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already checked in today"
        )
    
    health_activity = HealthActivity(
        user_id=current_user.id,
        activity_type=ActivityType.CHECKIN,
        mood_score=check_in.mood_score,
        sleep_hours=check_in.sleep_hours,
        water_intake=check_in.water_intake
    )
    
    health_activity.points_earned = calculate_points(health_activity)
    
    db.add(health_activity)
    db.commit()
    db.refresh(health_activity)
    
    # Update user's elixir score
    current_user.elixir_score += health_activity.points_earned
    db.commit()
    
    return health_activity

@router.get("/history", response_model=List[HealthActivitySchema])
async def get_activity_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10
):
    """
    Get user's health activity history.
    """
    activities = db.query(HealthActivity)\
        .filter(HealthActivity.user_id == current_user.id)\
        .order_by(HealthActivity.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return activities 