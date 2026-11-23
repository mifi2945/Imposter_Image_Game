# Files API

FastAPI service backed by the private Cloud Storage bucket
`impostor-image-game-514519-images`. `GET /` reports health. `POST /files/`
uploads a PNG, JPEG, or WebP image as multipart form data (`file`, `userId`,
`lobbyId`) and returns `{"imageKey": "..."}`. `GET /files/{image_key}` downloads
it; `DELETE /files/{image_key}` removes it. Images are limited to 10 MiB.

From this directory:

```bash
uv sync --locked
export FILES_BUCKET_NAME=impostor-image-game-514519-images
gcloud auth application-default login
uv run --locked uvicorn api.main:create_app --factory --reload --port 8003
```

From the repository root:

```bash
docker build -t files-api:local FilesApi
docker run --rm -p 127.0.0.1:8003:8080 files-api:local
```

Open [Swagger](http://localhost:8003/docs).
The Docker command above checks health and docs; image operations also need
`FILES_BUCKET_NAME` and Google application-default credentials inside the
container. The local `uv` command uses the credentials from
`gcloud auth application-default login`.

To enable bucket access in GKE, run once from the repository root with a
Google Cloud account allowed to change bucket IAM:

```bash
bash FilesApi/infra/grant-bucket-access.sh
```

The Kubernetes Deployment sets `FILES_BUCKET_NAME` and uses the `files-api`
Kubernetes ServiceAccount in the `files` namespace. The script gives only that
workload `Storage Object User` on the bucket through Workload Identity
Federation. No service-account key is stored in the cluster. The bucket must
already exist with uniform bucket-level access, and the cluster must have
Workload Identity Federation enabled. The script accepts `PROJECT_ID`,
`BUCKET_NAME`, `CLUSTER_NAME`, and `CLUSTER_REGION` environment variable
overrides for other environments; also change `FILES_BUCKET_NAME` in the
Deployment manifest when using a different bucket.

If the script reports that the cluster has no workload identity pool, enable
it first (a cluster-wide operation):

```bash
gcloud container clusters update imposter-cluster --region=us-central1 \
  --project=impostor-image-game-514519 \
  --workload-pool=impostor-image-game-514519.svc.id.goog
```

The service owns its `pyproject.toml` and `uv.lock`. Its Dockerfile uses Python
3.13 and uv and listens on port 8080.

In GKE, the Deployment supplies `ORCHESTRATOR_API_URL` with Orchestrator's
internal Kubernetes DNS name. Upload notification is not wired yet because
Orchestrator's `/game/upload` endpoint still returns 501. The Files API stores
`userId` and `lobbyId` as object metadata; it does not yet list by lobby or
validate image contents beyond MIME type and size. Add authentication before
exposing write or delete endpoints outside the cluster.

Submit `cloudbuild.yaml` with the repository root as the source context.
