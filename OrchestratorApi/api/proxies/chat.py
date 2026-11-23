from fastapi import Request

from ..config import Settings
from .base import ServiceProxy


class ChatProxy(ServiceProxy):
    async def send_message(self, lobby_id: int, message: str) -> None:
        """TODO: Chat API currently has only a health endpoint."""
        raise NotImplementedError("Chat message endpoint is not defined")


def get_chat_proxy(request: Request) -> ChatProxy:
    settings: Settings = request.app.state.settings
    if not settings.chat_api_url:
        raise RuntimeError("CHAT_API_URL must name the Chat service")
    return ChatProxy(request.app.state.http, settings.chat_api_url)
