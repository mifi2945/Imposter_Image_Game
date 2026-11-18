from enum import Enum
from uuid import UUID

from fastapi import APIRouter, FastAPI, HTTPException, status
from pydantic import BaseModel, Field



class Player(BaseModel):
    username: str
    favorite_minion: str | None = None


class GameState(str, Enum):
    WAITING_FOR_PLAYERS = "waiting_for_players"
    ASSIGNING_ROLES = "assigning_roles"
    PENDING_ANSWERS = "pending_answers"
    VOTING = "voting"


class Game(BaseModel):
    state: GameState = GameState.WAITING_FOR_PLAYERS


class UploadEvent(BaseModel):
    image_key: UUID = Field(alias="imageKey")
    user_id: int = Field(alias="userId")
    lobby_id: int = Field(alias="lobbyId")
