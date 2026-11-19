from fastapi import FastAPI


app = FastAPI(title="Files Service")


@app.get("/", tags=["Files"])
async def read_root():
    """Report that the service is running."""
    return {"service": "files", "status": "ok"}
