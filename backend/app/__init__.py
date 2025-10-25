# backend/app/__init__.py

from fastapi import FastAPI

app = FastAPI()

# Import routers
from .api.v1.router import router as api_router

# Include the API router
app.include_router(api_router)