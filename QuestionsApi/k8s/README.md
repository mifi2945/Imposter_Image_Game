# Questions API deployment

These manifests deploy the Questions API and a single-replica PostgreSQL
StatefulSet with a persistent volume claim. They do not create a GKE cluster.
The API currently receives PostgreSQL connection settings as environment
variables. On startup it applies any unapplied SQL files in
`QuestionsApi/api/migrations/`; the create, list, and delete endpoints use
PostgreSQL.

## Local Kubernetes

Install Docker, kubectl, and Minikube, then create and start the local cluster.
The cluster must have a default StorageClass for the Postgres volume claim.

From the repository root:

```sh
minikube start
docker build -t questions-api:local -f QuestionsApi/api/Dockerfile QuestionsApi/api
minikube image load questions-api:local
```

Create the namespace and database Secret, then deploy the manifests:

```sh
kubectl apply -f QuestionsApi/k8s/00-namespace.yaml
kubectl -n questions create secret generic questions-db-credentials \
  --from-literal=POSTGRES_PASSWORD="$(openssl rand -base64 32)"
kubectl apply -f QuestionsApi/k8s/
```

Access the API locally with:

```sh
kubectl -n questions port-forward service/questions-api 8080:80
```

Then open `http://localhost:8080/`. Keep the generated database password
somewhere safe; do not commit it to the repository.

## GKE deployment

Cloud Build deploys to GKE; it does not deploy to Cloud Run. Create the GKE
cluster and Artifact Registry repository in the same Google Cloud project, and
grant the Cloud Build service account permission to push images and deploy
workloads to the cluster.

After creating a regional GKE cluster, configure kubectl to use it:

```sh
gcloud container clusters get-credentials imposter-cluster \
  --region=us-central1
```

Create the `questions` namespace and a database password Secret before the
first Cloud Build deployment:

```sh
kubectl apply -f QuestionsApi/k8s/00-namespace.yaml
kubectl -n questions create secret generic questions-db-credentials \
  --from-literal=POSTGRES_PASSWORD="$(openssl rand -base64 32)"
```

Create the `imposter-repo` Artifact Registry repository in `us-central1` (or
change the substitutions in `cloudbuild.yaml`). Then submit from the
repository root:

```sh
gcloud builds submit --config=QuestionsApi/cloudbuild.yaml \
  --substitutions=_CLUSTER_NAME=imposter-cluster,_CLUSTER_LOCATION=us-central1 .
```

Set `_REGION` and `_AR_REPOSITORY` in `cloudbuild.yaml` to match the Artifact
Registry repository. `_CLUSTER_LOCATION` should match the GKE cluster's region.
Before each environment's first build, create the
`questions-db-credentials` Secret in the `questions` namespace. Cloud Build
applies the namespace and Postgres StatefulSet, waits for Postgres to become
ready, and then deploys the API.

The Kubernetes database uses a 1 GiB persistent volume claim; it is a single
instance and does not include automated backups or high availability.
