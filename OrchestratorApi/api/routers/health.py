from fastapi import APIRouter

router = APIRouter(tags=["Orchestrator"])


@router.get("/")
async def read_root():
    return {"service": "orchestrator", "status": "ok"}
