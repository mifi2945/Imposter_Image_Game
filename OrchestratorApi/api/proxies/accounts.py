from fastapi import Request

from ..config import Settings
from .base import ServiceProxy


class AccountsProxy(ServiceProxy):
    async def get_public_key(self) -> str:
        response = await self.client.get(f"{self.base_url}/public_key")
        response.raise_for_status()
        return response.json()

    async def award_points(self, username: str, points: int) -> None:
        """TODO: Accounts API does not yet expose an endpoint to award points."""
        raise NotImplementedError("Accounts points endpoint is not defined")


def get_accounts_proxy(request: Request) -> AccountsProxy:
    settings: Settings = request.app.state.settings
    if not settings.accounts_api_url:
        raise RuntimeError("ACCOUNTS_API_URL must name the Accounts service")
    return AccountsProxy(request.app.state.http, settings.accounts_api_url)
