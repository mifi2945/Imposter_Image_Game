from fastapi import FastAPI
from type import Account, AccountStat
from google.cloud import firestore
import os

app = FastAPI()
db = firestore.AsyncClient(project=os.environ.get("PROJECT", "impostor-image-game-514519"), 
                           database=os.environ.get("ACCOUNTS_DB", "accounts-api-db"))

@app.post("/sign_up")
async def sign_in(account: Account):
    pass

@app.get("/test_db")
async def test_db():
    doc = await db.collection("users").document("admin123").get()
    return doc.to_dict()