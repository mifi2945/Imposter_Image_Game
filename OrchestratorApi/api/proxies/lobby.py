from fastapi import Request

from ..config import Settings
from .base import ServiceProxy


class LobbyProxy(ServiceProxy):
    async def get_lobby(self, lobby_id: str) -> dict:
        response = await self.client.get(f"{self.base_url}/lobbies/{lobby_id}")
        response.raise_for_status()
        return response.json()

    async def start_game(self, game_id: int) -> None:
        """TODO: Agree on a request contract for Lobby's POST /game/startGame."""
        raise NotImplementedError("Lobby game-start request contract is not defined")


def get_lobby_proxy(request: Request) -> LobbyProxy:
    settings: Settings = request.app.state.settings
    if not settings.lobby_api_url:
        raise RuntimeError("LOBBY_API_URL must name the Lobby service")
    return LobbyProxy(request.app.state.http, settings.lobby_api_url)
