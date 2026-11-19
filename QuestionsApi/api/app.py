import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import fastapi
from fastapi.middleware.cors import CORSMiddleware
from database import apply_migrations
from routes import questions_router as questions


@asynccontextmanager
async def lifespan(_: fastapi.FastAPI) -> AsyncIterator[None]:
    await apply_migrations()
    yield


app = fastapi.FastAPI(lifespan=lifespan)
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

app.include_router(questions.router)

@app.get("/")
async def root():
    return {"message": "Questions service is running"}
