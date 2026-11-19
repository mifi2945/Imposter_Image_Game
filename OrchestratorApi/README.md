# Orchestrator API

FastAPI scaffold for game orchestration. `GET /` is a health endpoint; the
message, game, and vote handlers remain 501 stubs.

From this directory:

```bash
uv sync --locked
uv run --locked uvicorn api.router:app --reload --port 8002
```

From the repository root:

```bash
docker build -t orchestrator-api:local OrchestratorApi
docker run --rm -p 127.0.0.1:8002:8080 orchestrator-api:local
```

Open [Swagger](http://localhost:8002/docs).

The service owns its `pyproject.toml` and `uv.lock`. Its Dockerfile uses Python
3.13 and uv and listens on port 8080.

In GKE, the Deployment supplies `FILES_API_URL`, `LOBBY_API_URL`, and
`QUESTIONS_API_URL` with the other services' internal Kubernetes DNS names.
Future handlers should read these environment variables when making HTTP calls;
the current handlers are still stubs. Set them to local URLs when developing
outside the cluster.

Submit `cloudbuild.yaml` with the repository root as the source context.
