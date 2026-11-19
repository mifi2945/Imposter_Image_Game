## Choose the deployment target

```bash
gcloud auth list
gcloud projects list
# If the right account is missing:
gcloud auth login
```

Run these commands in Bash from the repository root. The cluster and repository
values below were checked in `impostor-image-game-514519`:

```bash
export PROJECT_ID="impostor-image-game-514519"
export CLUSTER_NAME="imposter-cluster"
export CLUSTER_REGION="us-central1"
export REGISTRY_REGION="us-central1"
export REPOSITORY="impostor-repo"

gcloud config set project "$PROJECT_ID"
gcloud container clusters list --project="$PROJECT_ID"
gcloud artifacts repositories list --project="$PROJECT_ID" --location="$REGISTRY_REGION"
```

Use the project ID, not its display name. An older project called
`impostor-image-game` has a different ID and is pending deletion.

NEEDED APIs:
* Cloud Build
* Artifact Registry
* Kubernetes Engine
SERVICE ACCOUNT PERMS:
* push images
* write Cloud Logging logs
* deploy into the cluster


## Build and deploy

From the repository root, using the variables above:

```bash
export DEPLOY_SUBSTITUTIONS="_REGION=${REGISTRY_REGION},_AR_REPOSITORY=${REPOSITORY},_CLUSTER_NAME=${CLUSTER_NAME},_CLUSTER_LOCATION=${CLUSTER_REGION}"

gcloud builds submit . --project="$PROJECT_ID" --region="$REGISTRY_REGION" --config=OrchestratorApi/cloudbuild.yml --substitutions="$DEPLOY_SUBSTITUTIONS"
gcloud builds submit . --project="$PROJECT_ID" --region="$REGISTRY_REGION" --config=FilesApi/cloudbuild.yml --substitutions="$DEPLOY_SUBSTITUTIONS"
```


To inspect the deployed services locally, install the GKE auth plugin if needed,
then obtain cluster credentials:

```bash
gcloud components install gke-gcloud-auth-plugin
gcloud container clusters get-credentials "$CLUSTER_NAME" --region="$CLUSTER_REGION" --project="$PROJECT_ID"
kubectl -n orchestrator get pods,services
kubectl -n files get pods,services
```

The Services use ClusterIP. Forward them locally in separate terminals:

```bash
kubectl -n orchestrator port-forward service/orchestrator-api 8002:80
kubectl -n files port-forward service/files-api 8003:80
```

The same localhost health and Swagger URLs now reach the deployed containers.
Inside the cluster, their addresses are
`http://orchestrator-api.orchestrator.svc.cluster.local` and
`http://files-api.files.svc.cluster.local`. Public ingress is not configured.

If a rollout fails, inspect the cause:

```bash
kubectl -n orchestrator describe pods
kubectl -n orchestrator logs deployment/orchestrator-api
kubectl -n files describe pods
kubectl -n files logs deployment/files-api
```

## Automatic deployment on pushes

The existing `accounts-api-trigger` already connects Cloud Build to
`mifi2945/Imposter_Image_Game` in the `global` trigger region. It watches pushes
to `main` and includes only `AccountsApi/**`. Reuse that connection and service
account for two service-specific triggers:

| Service | Included files | Build config |
| --- | --- | --- |
| Orchestrator | `OrchestratorApi/**` | `OrchestratorApi/cloudbuild.yml` |
| Files | `FilesApi/**` | `FilesApi/cloudbuild.yml` |

The existing `cloud-build@${PROJECT_ID}.iam.gserviceaccount.com` service account
has Artifact Registry Writer and Logging Writer on this project. The two new
configs also deploy to GKE, so grant that account Kubernetes Engine Developer
before creating the triggers:

```bash
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:cloud-build@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/container.developer"
```

From the repository root, create triggers matching the Accounts trigger:

```bash
export BUILD_SERVICE_ACCOUNT="projects/${PROJECT_ID}/serviceAccounts/cloud-build@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud builds triggers create github \
  --project="$PROJECT_ID" --region=global \
  --name=orchestrator-api-trigger \
  --repo-owner=mifi2945 --repo-name=Imposter_Image_Game \
  --branch-pattern='^main$' --included-files='OrchestratorApi/**' \
  --build-config=OrchestratorApi/cloudbuild.yml \
  --service-account="$BUILD_SERVICE_ACCOUNT"

gcloud builds triggers create github \
  --project="$PROJECT_ID" --region=global \
  --name=files-api-trigger \
  --repo-owner=mifi2945 --repo-name=Imposter_Image_Game \
  --branch-pattern='^main$' --included-files='FilesApi/**' \
  --build-config=FilesApi/cloudbuild.yml \
  --service-account="$BUILD_SERVICE_ACCOUNT"
```

Check them with:

```bash
gcloud builds triggers list --project="$PROJECT_ID" --region=global
```

Commit and push each service's source, `uv.lock`, Dockerfile, build config, and
manifests to `main`. A push changing `OrchestratorApi/**` or `FilesApi/**` then
starts only the matching build. The trigger uses the service account selected
when the trigger is created. The build configs already specify the cluster and
registry defaults, so no trigger substitutions are needed for this project.

## Dependency updates

From the relevant service directory, use `uv add PACKAGE` or
`uv lock --upgrade`, then commit both `pyproject.toml` and `uv.lock`.
The Docker build rejects a lockfile that is out of date.

References: [uv Docker integration](https://docs.astral.sh/uv/guides/integration/docker/)
and [Cloud Build deployment to GKE](https://docs.cloud.google.com/build/docs/deploying-builds/deploy-gke).
