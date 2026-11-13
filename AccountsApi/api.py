from fastapi import FastAPI, HTTPException, Request, Response, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.cloud import firestore
import os
import datetime

from AccountsApi.type import Account, AccountStat, AccountDB
from AccountsApi.pw_access import hash_password, verify_password
from AccountsApi.token_access import Token

app = FastAPI()
bearer_scheme = HTTPBearer()
db = firestore.AsyncClient(project=os.environ.get("PROJECT", "impostor-image-game-514519"), 
                           database=os.environ.get("ACCOUNTS_DB", "accounts-api-db"))

@app.post("/sign_up", status_code=status.HTTP_201_CREATED)
async def sign_up(account: Account):
    user = account.username
    doc = await db.collection("users").document(user).get()
    if doc.exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    pw = account.password
    tokens = Token.gen_tokens(user, "user")

    # save to db
    doc = AccountDB(
        password=hash_password(pw),
        refresh_token=tokens['hash_refresh_token'],
        expires=(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)).isoformat()
    ).model_dump()
    await db.collection("users").document(user).set(doc)

    return {"access_token": tokens["access_token"],
            "refresh_token": tokens["raw_refresh_token"]}

@app.post("/sign_in", status_code=status.HTTP_200_OK)
async def sign_in(account: Account):
    user = account.username
    pw = account.password
    doc = await db.collection("users").document(user).get()

    # user does not exist / wrong password
    if not doc.exists or not verify_password(pw, doc.get("password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username or password"
        )

    tokens = Token.gen_tokens(user, "user")
    refresh_token_update = {
        "refresh_token": tokens['hash_refresh_token'],
        "expires": (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)).isoformat()
    }
    await db.collection("users").document(user).update(refresh_token_update)
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["raw_refresh_token"]
    }
    

@app.get("/public_key")
async def get_public_key():
    return Token.get_public_key()



# @app.get("/test_db")
# async def test_db():
#     doc = await db.collection("users").document("admin123").get()
#     return doc.to_dict()

# @app.get("/test_token_verify")
# async def test_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
#     claims = Token.verify_access_token(credentials.credentials)

#     if claims is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Access token invalid or expired"
#         )
#     return claims