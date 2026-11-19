from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from google.api_core.exceptions import NotFound

from api.router import MAX_IMAGE_BYTES, app
from api.storage import ImageStore, get_image_store


class FakeStore:
    def __init__(self):
        self.images = {}

    def upload(self, image_key, data, content_type, user_id, lobby_id):
        self.images[image_key] = (data, content_type, user_id, lobby_id)

    def download(self, image_key):
        if image_key not in self.images:
            raise NotFound("missing")
        data, content_type, _, _ = self.images[image_key]
        return data, content_type

    def delete(self, image_key):
        if image_key not in self.images:
            raise NotFound("missing")
        del self.images[image_key]


@pytest.fixture
def client_and_store():
    store = FakeStore()
    app.dependency_overrides[get_image_store] = lambda: store
    try:
        with TestClient(app) as client:
            yield client, store
    finally:
        app.dependency_overrides.clear()


def test_upload_download_and_delete(client_and_store):
    client, store = client_and_store
    response = client.post(
        "/files/",
        data={"userId": "7", "lobbyId": "12"},
        files={"file": ("picture.png", b"image bytes", "image/png")},
    )
    assert response.status_code == 201
    image_key = UUID(response.json()["imageKey"])
    assert store.images[image_key] == (b"image bytes", "image/png", 7, 12)

    downloaded = client.get(f"/files/{image_key}")
    assert downloaded.status_code == 200
    assert downloaded.content == b"image bytes"
    assert downloaded.headers["content-type"] == "image/png"
    assert downloaded.headers["cache-control"] == "private, no-store"

    assert client.delete(f"/files/{image_key}").status_code == 204
    assert client.get(f"/files/{image_key}").status_code == 404


def test_upload_rejects_invalid_type_and_oversize(client_and_store):
    client, store = client_and_store
    fields = {"userId": "7", "lobbyId": "12"}
    assert client.post(
        "/files/", data=fields, files={"file": ("file.txt", b"text", "text/plain")}
    ).status_code == 415
    assert client.post(
        "/files/", data=fields, files={"file": ("empty.png", b"", "image/png")}
    ).status_code == 400
    assert client.post(
        "/files/",
        data=fields,
        files={"file": ("huge.png", b"x" * (MAX_IMAGE_BYTES + 1), "image/png")},
    ).status_code == 413
    assert not store.images


def test_gcs_adapter_uses_private_uuid_object_and_upload_metadata():
    class FakeBlob:
        def upload_from_string(self, data, **kwargs):
            self.upload = (data, kwargs)

    class FakeBucket:
        def blob(self, name):
            self.name = name
            self.created_blob = FakeBlob()
            return self.created_blob

    class FakeClient:
        def bucket(self, name):
            self.bucket_name = name
            self.created_bucket = FakeBucket()
            return self.created_bucket

    fake_client = FakeClient()
    store = ImageStore("test-bucket", client=fake_client)
    image_key = UUID("12345678-1234-1234-1234-123456789abc")
    store.upload(image_key, b"data", "image/png", user_id=7, lobby_id=12)

    assert fake_client.bucket_name == "test-bucket"
    assert fake_client.created_bucket.name == f"images/{image_key}"
    assert fake_client.created_bucket.created_blob.metadata == {
        "user_id": "7", "lobby_id": "12"
    }
    assert fake_client.created_bucket.created_blob.upload == (
        b"data", {"content_type": "image/png", "if_generation_match": 0}
    )
