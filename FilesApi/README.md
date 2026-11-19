# Files API

Minimal FastAPI service ready for container deployment. `GET /` returns
`{"service": "files", "status": "ok"}`. File storage, retrieval, and upload
notifications are not implemented yet.

From this directory:

```bash
uv sync --locked
uv run --locked uvicorn api.router:app --reload --port 8003
```

From the repository root:

```bash
docker build -t files-api:local FilesApi
docker run --rm -p 127.0.0.1:8003:8080 files-api:local
```

Open [Swagger](http://localhost:8003/docs).

The service owns its `pyproject.toml` and `uv.lock`. Its Dockerfile uses Python
3.13 and uv and listens on port 8080.

In GKE, the Deployment supplies `ORCHESTRATOR_API_URL` with Orchestrator's
internal Kubernetes DNS name. The upload-notification handler can read this
environment variable when it is implemented. Set it to a local URL when
developing outside the cluster.

Submit `cloudbuild.yaml` with the repository root as the source context.
