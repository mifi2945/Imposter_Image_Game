import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Files Service")
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


@app.get("/", tags=["Files"])
async def read_root():
    """Report that the service is running."""
    return {"service": "files", "status": "ok"}
