# Orchestrator API

FastAPI scaffold for the Orchestrator service. `GET /` is a health endpoint; the
message, game, and vote handlers remain 501 stubs. `POST /game/upload` accepts
`image_key`, `user_id`, and `lobby_id` in its JSON body.

From this directory:

```bash
uv sync --locked
uv run --locked uvicorn api.main:create_app --factory --reload --port 8002
```

From the repository root:

```bash
docker build -t orchestrator-api:local OrchestratorApi
docker run --rm -p 127.0.0.1:8002:8080 orchestrator-api:local
```

Open [Swagger](http://localhost:8002/docs).

The service owns its `pyproject.toml` and `uv.lock`. Its Dockerfile uses Python
3.13 and uv and listens on port 8080.

`api.main` creates the app and a shared HTTP client. Routes live in
`api.routers`; `api.proxies` holds downstream service clients. Set
`FILES_API_URL`, `LOBBY_API_URL`, `QUESTIONS_API_URL`, `ACCOUNTS_API_URL`, and
`CHAT_API_URL` to the services' base URLs when developing locally. The GKE
Deployment supplies the first four using internal Kubernetes DNS names. Chat
has no Kubernetes Service or message endpoint yet, so its proxy remains an
explicit stub and `CHAT_API_URL` is not configured in GKE. The Accounts points
and Lobby game-start proxy methods also await their request contracts. Existing
Orchestrator game, message, and vote handlers still return 501. The Questions
round endpoint currently requires an admin bearer token, which callers must
pass to its proxy method.

Submit `cloudbuild.yaml` with the repository root as the source context.
