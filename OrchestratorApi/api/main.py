from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings, get_settings
from .routers import game, health, message, votes


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: Settings = app.state.settings
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(30.0, pool=5.0),
        limits=httpx.Limits(
            max_connections=settings.max_connections,
            max_keepalive_connections=settings.max_keepalive_connections,
        ),
    ) as client:
        app.state.http = client
        yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Orchestrator Service", lifespan=lifespan)
    app.state.settings = settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            origin.strip()
            for origin in settings.cors_origins.split(",")
            if origin.strip()
        ],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    app.include_router(message.router)
    app.include_router(game.router)
    app.include_router(votes.router)
    return app
