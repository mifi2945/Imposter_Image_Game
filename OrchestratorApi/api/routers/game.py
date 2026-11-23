from fastapi import APIRouter, HTTPException, status

from ..models import UploadEvent

router = APIRouter(prefix="/game", tags=["Game"])


@router.post("/answer", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def send_game_answers():
    """TODO: Fetch players' images and send all answers to the lobby's users."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Sharing game answers is not implemented yet.",
    )


@router.post(
    "/upload",
    status_code=status.HTTP_200_OK,
    responses={501: {"description": "Upload handling is not implemented yet."}},
)
async def handle_upload(event: UploadEvent):
    """TODO: Record the file service's upload event as a user's answer; return 200."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Upload handling is not implemented yet.",
    )


@router.post("/startGame/{game_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def start_game(game_id: int):
    """TODO: Start the specified game and assign player roles."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Starting a game is not implemented yet.",
    )
