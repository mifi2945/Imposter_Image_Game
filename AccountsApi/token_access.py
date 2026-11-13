import datetime
import hashlib
import secrets
import jwt
import os


with open(os.environ.get("PRIVATE_KEY_PATH", "keys/ec_private.pem"), "rb") as f:
    PRIVATE_KEY = f.read()

with open(os.environ.get("PUBLIC_KEY_PATH", "keys/ec_public.pem"), "rb") as f:
    PUBLIC_KEY = f.read()

ALG = os.environ.get("KEY_ALGORITHM", "ES256")

class Token:

    @staticmethod
    def get_public_key():
        return PUBLIC_KEY


    @staticmethod
    def create_access_token(user: str, role: str)->str:
        now = datetime.datetime.now(datetime.timezone.utc)
        claims = {
            "sub": user,
            "exp": (now + datetime.timedelta(minutes=15)).isoformat(),
            "role": role
        }
        return jwt.encode(claims, PRIVATE_KEY, algorithm=ALG)
    
    @staticmethod
    def verify_access_token(token: str)->dict | None:
        try:
            return jwt.decode(token, PUBLIC_KEY, algorithms=[ALG], 
                              options={"require": ["sub", "exp", "role"]},
                              leeway=5)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def gen_tokens(user: str, role: str)->dict:
        access_token = Token.create_access_token(user, role)

        raw_refresh_token = secrets.token_urlsafe(32)
        hash_refresh_token = Token.hash_token(raw_refresh_token)

        return {
            "access_token": access_token,
            "raw_refresh_token": raw_refresh_token,
            "hash_refresh_token": hash_refresh_token
        }

    @staticmethod
    def hash_token(token: str):
        return hashlib.sha256(token.encode()).hexdigest()