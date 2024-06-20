from fastapi import APIRouter
from .endpoints import health, auth

router = APIRouter(
    prefix="/v1",
)
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
