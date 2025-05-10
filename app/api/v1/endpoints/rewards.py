from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.reward import Reward, RewardTransaction
from app.schemas.reward import (
    Reward as RewardSchema,
    RewardCreate,
    RewardTransaction as RewardTransactionSchema,
    RewardTransactionCreate
)

router = APIRouter()

@router.get("/catalog", response_model=List[RewardSchema])
async def get_reward_catalog(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10
):
    """
    Get available rewards catalog.
    """
    rewards = db.query(Reward)\
        .filter(Reward.is_active == True)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return rewards

@router.post("/redeem", response_model=RewardTransactionSchema)
async def redeem_reward(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    transaction: RewardTransactionCreate
):
    """
    Redeem points for a reward.
    """
    # Get the reward
    reward = db.query(Reward).filter(Reward.id == transaction.reward_id).first()
    if not reward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reward not found"
        )
    
    # Check if reward is active
    if not reward.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reward is no longer available"
        )
    
    # Check if user has enough points
    if current_user.elixir_score < reward.points_required:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough points to redeem this reward"
        )
    
    # Create transaction
    reward_transaction = RewardTransaction(
        user_id=current_user.id,
        reward_id=reward.id,
        points_spent=reward.points_required
    )
    
    # Update user's points
    current_user.elixir_score -= reward.points_required
    
    db.add(reward_transaction)
    db.commit()
    db.refresh(reward_transaction)
    
    return reward_transaction

@router.get("/transactions", response_model=List[RewardTransactionSchema])
async def get_reward_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10
):
    """
    Get user's reward redemption history.
    """
    transactions = db.query(RewardTransaction)\
        .filter(RewardTransaction.user_id == current_user.id)\
        .order_by(RewardTransaction.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return transactions

@router.post("/admin/add", response_model=RewardSchema)
async def add_reward(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    reward: RewardCreate
):
    """
    Add a new reward to the catalog (Admin only).
    """
    # In a real app, you'd check if the user is an admin
    new_reward = Reward(**reward.dict())
    db.add(new_reward)
    db.commit()
    db.refresh(new_reward)
    return new_reward 