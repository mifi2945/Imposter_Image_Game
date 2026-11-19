import os

import logging
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import Response
from google.api_core.exceptions import GoogleAPICallError, NotFound
from pydantic import BaseModel, Field

from .storage import ImageStore, get_image_store
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
logger = logging.getLogger(__name__)

MAX_IMAGE_BYTES = 10 * 1024 * 1024 # 10 Mibs
IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


# Random UUIDs for image keys = no concern of random users accessing targeted images
class UploadedImage(BaseModel):
    image_key: UUID = Field(alias="imageKey")


@app.get("/", tags=["Files"])
async def read_root():
    """Report that the service is running."""
    return {"service": "files", "status": "ok"}


@app.post("/files/", response_model=UploadedImage, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(),
    user_id: int = Form(alias="userId"),
    lobby_id: int = Form(alias="lobbyId"),
    store: ImageStore = Depends(get_image_store),
):
    """Store an image and return its key for later retrieval."""
    if file.content_type not in IMAGE_TYPES:
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Unsupported image type")

    data = await file.read(MAX_IMAGE_BYTES + 1)
    if not data:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Image is empty")
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(status.HTTP_413_CONTENT_TOO_LARGE, "Image exceeds 10 MiB")

    image_key = uuid4()
    try:
        await run_in_threadpool(
            store.upload, image_key, data, file.content_type, user_id, lobby_id
        )
    except GoogleAPICallError:
        logger.exception("Could not upload image %s", image_key)
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Image storage unavailable") from None
    return UploadedImage(imageKey=image_key)


@app.get("/files/{image_key}")
async def download_image(
    image_key: UUID, store: ImageStore = Depends(get_image_store)
):
    """Return a stored image by key."""
    try:
        data, content_type = await run_in_threadpool(store.download, image_key)
    except NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Image not found") from None
    except GoogleAPICallError:
        logger.exception("Could not download image %s", image_key)
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Image storage unavailable") from None
    return Response(
        content=data,
        media_type=content_type,
        headers={"Cache-Control": "private, no-store"},
    )


@app.delete("/files/{image_key}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    image_key: UUID, store: ImageStore = Depends(get_image_store)
):
    """Remove a stored image by key."""
    try:
        await run_in_threadpool(store.delete, image_key)
    except NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Image not found") from None
    except GoogleAPICallError:
        logger.exception("Could not delete image %s", image_key)
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Image storage unavailable") from None
