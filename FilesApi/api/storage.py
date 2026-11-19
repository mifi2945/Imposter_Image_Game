"""Cloud Storage access for game images."""

import os
from functools import lru_cache
from uuid import UUID

from google.cloud import storage


class ImageStore:
    def __init__(self, bucket_name: str, client: storage.Client | None = None):
        self.bucket = (client or storage.Client()).bucket(bucket_name)

    @staticmethod
    def object_name(image_key: UUID) -> str:
        return f"images/{image_key}"

    def upload(
        self,
        image_key: UUID,
        data: bytes,
        content_type: str,
        user_id: int,
        lobby_id: int,
    ) -> None:
        blob = self.bucket.blob(self.object_name(image_key))
        blob.metadata = {"user_id": str(user_id), "lobby_id": str(lobby_id)}
        blob.upload_from_string(
            data,
            content_type=content_type,
            if_generation_match=0,
        )

    def download(self, image_key: UUID) -> tuple[bytes, str]:
        blob = self.bucket.blob(self.object_name(image_key))
        blob.reload()
        return blob.download_as_bytes(), blob.content_type or "application/octet-stream"

    def delete(self, image_key: UUID) -> None:
        self.bucket.blob(self.object_name(image_key)).delete()


@lru_cache
def get_image_store() -> ImageStore:
    bucket_name = os.environ.get("FILES_BUCKET_NAME")
    if not bucket_name:
        raise RuntimeError("FILES_BUCKET_NAME must name the Cloud Storage bucket")
    return ImageStore(bucket_name)
