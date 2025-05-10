from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class RewardBase(BaseModel):
    name: str
    description: str
    points_required: int
    brand: str

class RewardCreate(RewardBase):
    pass

class Reward(RewardBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class RewardTransactionBase(BaseModel):
    reward_id: int

class RewardTransactionCreate(RewardTransactionBase):
    pass

class RewardTransaction(RewardTransactionBase):
    id: int
    user_id: int
    points_spent: int
    created_at: datetime
    reward: Reward

    class Config:
        orm_mode = True 