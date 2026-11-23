"""Client boundary for notifying Orchestrator about uploaded images."""

import httpx
from fastapi import Request

from ..config import Settings
from ..models import UploadEvent


class OrchestratorProxy:
    def __init__(self, client: httpx.AsyncClient, base_url: str):
        self.client = client
        self.base_url = base_url.rstrip("/")

    async def notify_upload(self, event: UploadEvent) -> None:
        response = await self.client.post(
            f"{self.base_url}/game/upload",
            json=event.model_dump(mode="json"),
        )
        response.raise_for_status()


def get_orchestrator_proxy(request: Request) -> OrchestratorProxy:
    settings: Settings = request.app.state.settings
    if not settings.orchestrator_api_url:
        raise RuntimeError("ORCHESTRATOR_API_URL must name the Orchestrator service")
    return OrchestratorProxy(request.app.state.http, settings.orchestrator_api_url)
