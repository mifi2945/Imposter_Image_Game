from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/message", tags=["Messages"])


@router.post("/image", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def send_image_message():
    """TODO: Send an image message."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Image messaging is not implemented yet.",
    )


@router.post("/chat", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def send_chat_message():
    """TODO: Send a chat message."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Chat messaging is not implemented yet.",
    )
