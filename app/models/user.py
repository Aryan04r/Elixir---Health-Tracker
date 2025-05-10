from sqlalchemy import Boolean, Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from app.core.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    goals = Column(String)  # We can store this as JSON string or create a separate table
    is_active = Column(Boolean, default=True)
    elixir_score = Column(Integer, default=0)
    created_at = Column(Date)

    # Relationship with HealthActivity
    health_activities = relationship("HealthActivity", back_populates="user")

    # Relationship with RewardTransaction
    reward_transactions = relationship("RewardTransaction", back_populates="user")