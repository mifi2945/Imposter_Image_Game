from fastapi import Request

from ..config import Settings
from .base import ServiceProxy


class QuestionsProxy(ServiceProxy):
    async def get_round_question(self, admin_access_token: str) -> dict:
        """Questions API currently requires an admin bearer token for this route."""
        response = await self.client.get(
            f"{self.base_url}/questions/round",
            headers={"Authorization": f"Bearer {admin_access_token}"},
        )
        response.raise_for_status()
        return response.json()


def get_questions_proxy(request: Request) -> QuestionsProxy:
    settings: Settings = request.app.state.settings
    if not settings.questions_api_url:
        raise RuntimeError("QUESTIONS_API_URL must name the Questions service")
    return QuestionsProxy(request.app.state.http, settings.questions_api_url)
