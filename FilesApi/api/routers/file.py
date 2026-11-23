import logging
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import Response
from google.api_core.exceptions import GoogleAPICallError, NotFound
from ..models import UploadEvent, UploadedImage
from ..proxies.orchestrator import OrchestratorProxy, get_orchestrator_proxy
from ..storage import ImageStore, get_image_store


logger = logging.getLogger(__name__)

MAX_IMAGE_BYTES = 10 * 1024 * 1024 # 10 MiB
IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


router = APIRouter(prefix="/files", tags=["Files"])



@router.post("/", response_model=UploadedImage, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(),
    user_id: int = Form(),
    lobby_id: int = Form(),
    store: ImageStore = Depends(get_image_store),
    orchestrator_proxy: OrchestratorProxy = Depends(get_orchestrator_proxy),
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

    await orchestrator_proxy.notify_upload(
        UploadEvent(
            image_key=image_key,
            user_id=user_id,
            lobby_id=lobby_id,
        )
    )
    return UploadedImage(image_key=image_key)


@router.get("/{image_key}")
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



@router.delete("/{image_key}", status_code=status.HTTP_204_NO_CONTENT)
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
