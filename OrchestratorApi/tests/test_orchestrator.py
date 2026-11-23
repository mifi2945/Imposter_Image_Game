import asyncio
from uuid import UUID

import httpx
import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from api.config import Settings
from api.main import create_app
from api.proxies.accounts import AccountsProxy
from api.proxies.chat import ChatProxy
from api.proxies.files import FilesProxy, get_files_proxy
from api.proxies.lobby import LobbyProxy
from api.proxies.questions import QuestionsProxy


IMAGE_KEY = UUID("12345678-1234-1234-1234-123456789abc")


def test_health_and_existing_route_stubs():
    with TestClient(create_app()) as client:
        assert client.get("/").json() == {"service": "orchestrator", "status": "ok"}
        assert client.get("/openapi.json").json()["info"]["title"] == "Orchestrator Service"

        for path in (
            "/message/image",
            "/message/chat",
            "/game/answer",
            "/game/startGame/1",
            "/votes",
        ):
            assert client.post(path).status_code == 501

        assert client.post("/game/upload", json={}).status_code == 422
        assert client.post(
            "/game/upload",
            json={"imageKey": str(IMAGE_KEY), "userId": 1, "lobbyId": 2},
        ).status_code == 422
        response = client.post(
            "/game/upload",
            json={"image_key": str(IMAGE_KEY), "user_id": 1, "lobby_id": 2},
        )
        assert response.status_code == 501


def test_proxy_factory_uses_app_settings_and_shared_client():
    app = create_app()
    app.state.settings = Settings(files_api_url=None)
    request = Request({"type": "http", "app": app})

    with pytest.raises(RuntimeError, match="FILES_API_URL"):
        get_files_proxy(request)

    app.state.settings = Settings(files_api_url="http://files.local/")
    with TestClient(app):
        proxy = get_files_proxy(request)
        assert proxy.client is app.state.http
        assert proxy.base_url == "http://files.local"


def test_uppercase_service_url_environment_variable(monkeypatch):
    monkeypatch.setenv("FILES_API_URL", "http://files.from-env")
    assert Settings().files_api_url == "http://files.from-env"


def test_known_proxy_routes_and_auth_header():
    calls = []

    def handle(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if request.url.path == f"/files/{IMAGE_KEY}" and request.method == "GET":
            return httpx.Response(200, content=b"image", headers={"content-type": "image/png"})
        if request.url.path == "/public_key":
            return httpx.Response(200, json="PUBLIC KEY")
        if request.url.path == "/lobbies/42":
            return httpx.Response(200, json={"code": "ABCD"})
        if request.url.path == "/questions/round":
            return httpx.Response(200, json={"imposter_question": {"id": 1}})
        return httpx.Response(204)

    async def exercise():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handle)) as client:
            files = FilesProxy(client, "http://files.local/")
            assert await files.get_image(IMAGE_KEY) == (b"image", "image/png")
            await files.delete_image(IMAGE_KEY)
            assert await LobbyProxy(client, "http://lobby.local").get_lobby("42") == {"code": "ABCD"}
            assert await QuestionsProxy(client, "http://questions.local").get_round_question("token") == {
                "imposter_question": {"id": 1}
            }
            assert await AccountsProxy(client, "http://accounts.local").get_public_key() == "PUBLIC KEY"
            with pytest.raises(NotImplementedError, match="Chat message endpoint"):
                await ChatProxy(client, "http://chat.local").send_message(1, "hello")

    asyncio.run(exercise())

    assert [(request.method, request.url.path) for request in calls] == [
        ("GET", f"/files/{IMAGE_KEY}"),
        ("DELETE", f"/files/{IMAGE_KEY}"),
        ("GET", "/lobbies/42"),
        ("GET", "/questions/round"),
        ("GET", "/public_key"),
    ]
    assert calls[3].headers["authorization"] == "Bearer token"
