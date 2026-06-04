"""
StatEdge Pro - Main Application Entry Point.

This is the entry point for the StatEdge Pro application.
It initializes the FastAPI application and includes all routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="StatEdge Pro API",
    description="AI-powered sports analytics platform for teams and professional bettors",
    version="1.0.0"
)

# Configure CORS
origins = [
    os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
from src.api.main import router as api_router
app.include_router(api_router)

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {
        "status": "healthy",
        "service": "StatEdge Pro API",
        "version": "1.0.0",
        "environment": os.getenv("APP_ENV", "development")
    }

@app.get("/")
async def root():
    """
    Root endpoint providing API documentation.
    """
    return {
        "message": "Welcome to StatEdge Pro API",
        "documentation": "https://statedge-pro.com/docs",
        "endpoints": {
            "health": "/health",
            "analytics": "/api/v1/analytics",
            "value-finder": "/api/v1/value-finder",
            "teams": "/api/v1/teams",
            "players": "/api/v1/players",
            "games": "/api/v1/games",
            "reports": "/api/v1/reports",
            "data-feeds": "/api/v1/data-feeds",
            "users": "/api/v1/users",
            "api-keys": "/api/v1/api-keys"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
