from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    max_connections: int = Field(default=8, gt=0)
    max_keepalive_connections: int = Field(default=4, ge=0)
    files_api_url: str | None = None
    lobby_api_url: str | None = None
    questions_api_url: str | None = None
    accounts_api_url: str | None = None
    chat_api_url: str | None = None
    cors_origins: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
