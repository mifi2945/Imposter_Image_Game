from fastapi import APIRouter

router = APIRouter(tags=["Files"])


@router.get("/")
async def read_root():
    """Report that the service is running."""
    return {"service": "files", "status": "ok"}