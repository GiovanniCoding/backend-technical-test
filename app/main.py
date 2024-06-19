from fastapi import FastAPI
from app.api.v1.router import router as api_v1_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para gestionar usuarios e ítems",
    version="1.0.0",
)

# Mounting the API router
app.include_router(api_v1_router, prefix="/api/v1")
