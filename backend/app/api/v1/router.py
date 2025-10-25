from fastapi import APIRouter
from .endpoints import auth, codex, health

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(codex.router, prefix="/codex", tags=["codex"])
router.include_router(health.router, prefix="/health", tags=["health"])