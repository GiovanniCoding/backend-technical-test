from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["health"])
async def get_health_status():
    """
    Endpoint to check the health status of the API
    """
    return {"status": "Ok"}
