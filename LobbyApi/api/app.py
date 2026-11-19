import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.lobby_router import router as lobby_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.environ.get("CORS_ORIGINS", "").split(",")
        if origin.strip()
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(lobby_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Lobby service is running"}
