from fastapi import FastAPI

from routes.lobby_router import router as lobby_router

app = FastAPI()
app.include_router(lobby_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Lobby service is running"}
