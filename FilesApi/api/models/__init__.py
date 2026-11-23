"""Models used by the Files API and its service clients."""

from uuid import UUID

from pydantic import BaseModel


class UploadEvent(BaseModel):
    """Payload accepted by Orchestrator's POST /game/upload endpoint."""

    image_key: UUID
    user_id: int
    lobby_id: int


class UploadedImage(BaseModel):
    image_key: UUID
