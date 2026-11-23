from uuid import UUID

from fastapi import Request

from ..config import Settings
from .base import ServiceProxy


class FilesProxy(ServiceProxy):
    async def get_image(self, image_key: UUID) -> tuple[bytes, str]:
        """Fetch image bytes and their content type from Files API."""
        response = await self.client.get(f"{self.base_url}/files/{image_key}")
        response.raise_for_status()
        return response.content, response.headers["content-type"]

    async def delete_image(self, image_key: UUID) -> None:
        response = await self.client.delete(f"{self.base_url}/files/{image_key}")
        response.raise_for_status()


def get_files_proxy(request: Request) -> FilesProxy:
    settings: Settings = request.app.state.settings
    if not settings.files_api_url:
        raise RuntimeError("FILES_API_URL must name the Files service")
    return FilesProxy(request.app.state.http, settings.files_api_url)
