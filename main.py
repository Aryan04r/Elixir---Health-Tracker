from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import users
from app.core.init_db import init_db
from app.api.v1.endpoints import health_activities
from app.models import User, HealthActivity
from app.api.v1.endpoints import rewards

app = FastAPI(
    title="Elixir Health Rewards API",
    description="Backend service for tracking health activities and rewarding users",
    version="1.0.0"
)

# Initialize database
init_db()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(health_activities.router, prefix="/api/v1/health", tags=["health"])
app.include_router(rewards.router, prefix="/api/v1/rewards", tags=["rewards"])
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 