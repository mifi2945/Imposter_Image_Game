import fastapi
from routes import questions_router as questions

app = fastapi.FastAPI()

app.include_router(questions.router)

@app.get("/")
async def root():
    return {"message": "Questions service is running"}
