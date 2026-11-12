from fastapi import FastAPI
from type import Account, AccountStat
from google.cloud import firestore

app = FastAPI()
db = firestore.AsyncClient()

@app.post("/sign_up")
async def sign_in(account: Account):
    pass

@app.get("/test_db")
async def test_db():
    doc = await db.collection("users").document("admin123").get()
    return doc.to_dict()