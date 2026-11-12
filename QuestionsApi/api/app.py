from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import fastapi
from database import apply_migrations
from routes import questions_router as questions


@asynccontextmanager
async def lifespan(_: fastapi.FastAPI) -> AsyncIterator[None]:
    await apply_migrations()
    yield


app = fastapi.FastAPI(lifespan=lifespan)

app.include_router(questions.router)

@app.get("/")
async def root():
    return {"message": "Questions service is running"}
