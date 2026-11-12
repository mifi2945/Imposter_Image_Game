# Questions API deployment

These manifests deploy the Questions API and a single-replica PostgreSQL
StatefulSet with a persistent volume claim. They do not create a GKE cluster.
The API currently receives PostgreSQL connection settings as environment
variables, but its routes do not yet read from the database.

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

After creating a regional GKE cluster, configure kubectl to use it:

```sh
gcloud container clusters get-credentials questions-cluster \
  --region=us-central1
```

Create the `questions` namespace and a database password Secret before the
first Cloud Build deployment:

```sh
kubectl apply -f QuestionsApi/k8s/00-namespace.yaml
kubectl -n questions create secret generic questions-db-credentials \
  --from-literal=POSTGRES_PASSWORD="$(openssl rand -base64 32)"
```

Create the Artifact Registry repository and a GKE cluster in the same project.
The Cloud Build service account needs permission to push images and deploy to
that cluster. Then submit from the repository root:

```sh
gcloud builds submit --config=QuestionsApi/cloudbuild.yaml \
  --substitutions=_CLUSTER_NAME=questions-cluster,_CLUSTER_LOCATION=us-central1 .
```

Set `_REGION` and `_AR_REPOSITORY` in `cloudbuild.yaml` to match the Artifact
Registry repository. `_CLUSTER_LOCATION` should match the GKE cluster's region.

The Kubernetes database uses a 1 GiB persistent volume claim; it is a single
instance and does not include automated backups or high availability.
