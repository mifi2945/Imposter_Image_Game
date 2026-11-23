"""Client boundary for notifying Orchestrator about uploaded images."""

from uuid import UUID

import httpx
from fastapi import Request
from pydantic import BaseModel, Field

from ..config import Settings


class UploadEvent(BaseModel):
    """Payload accepted by Orchestrator's POST /game/upload endpoint."""

    image_key: UUID = Field(alias="imageKey")
    user_id: int = Field(alias="userId")
    lobby_id: int = Field(alias="lobbyId")


class OrchestratorProxy:
    def __init__(self, client: httpx.AsyncClient, base_url: str):
        self.client = client
        self.base_url = base_url.rstrip("/")

    async def notify_upload(self, event: UploadEvent) -> None:
        response = await self.client.post(
            f"{self.base_url}/game/upload",
            json=event.model_dump(by_alias=True, mode="json"),
        )
        response.raise_for_status()


def get_orchestrator_proxy(request: Request) -> OrchestratorProxy:
    settings: Settings = request.app.state.settings
    if not settings.orchestrator_api_url:
        raise RuntimeError("ORCHESTRATOR_API_URL must name the Orchestrator service")
    return OrchestratorProxy(request.app.state.http, settings.orchestrator_api_url)
