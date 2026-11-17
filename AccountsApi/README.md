# Accounts API

## Developer Usage
`cd` into `AccountsApi` and make sure all developer packages are installed easily with:

```bash
uv venv
uv sync
```

Then, run the following:

```bash
fastapi dev api.py
```

After which you can go to `localhost:8000/docs` to use Swagger to test all of the different endpoints to understand how they work.

Keep in mind you have to be authenticated with `gcloud auth application-default login` to connect to the Database while developing locally.