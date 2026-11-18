from enum import Enum
from uuid import UUID

from fastapi import APIRouter, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from models import *



app = FastAPI(title="Orchestration Service")

home_router = APIRouter(tags=["Orchestration"])
message_router = APIRouter(prefix="/message", tags=["Messages"])
game_router = APIRouter(prefix="/game", tags=["Game"])
vote_router = APIRouter(prefix="/votes", tags=["Votes"])


@home_router.get("/")
async def read_root():
    return {"service": "orchestration", "status": "ok"}



@message_router.post("/image", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def send_image_message():
    """TODO: Send an image message."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Image messaging is not implemented yet.",
    )


@message_router.post("/chat", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def send_chat_message():
    """TODO: Send a chat message."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Chat messaging is not implemented yet.",
    )


@game_router.post("/answer", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def send_game_answers():
    """TODO: Fetch players' images and send all answers to the lobby's users."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Sharing game answers is not implemented yet.",
    )


@game_router.post(
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


@game_router.post("/startGame/{game_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def start_game(game_id: int):
    """TODO: Start the specified game and assign player roles."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Starting a game is not implemented yet.",
    )


@vote_router.post("", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def submit_vote():
    """TODO: Record a player's vote for the impostor."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Voting is not implemented yet.",
    )


app.include_router(home_router)
app.include_router(message_router)
app.include_router(game_router)
app.include_router(vote_router)


