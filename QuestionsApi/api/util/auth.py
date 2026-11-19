from typing import Annotated
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import boto3
import time

from pydantic import BaseModel, ConfigDict, Field
from pydantic_core import ValidationError

app = FastAPI()
security = HTTPBearer()


def read_public_key() -> bytes:
    client = boto3.client(
        service_name="secretsmanager",
        region_name="us-central1"
    )
    try:
        response = client.get_secret_value(SecretId="accountsapi-es-public")
    except client.exceptions.ResourceNotFoundException:
        raise RuntimeError(f"Secret not found: accountsapi-es-public")
    except client.exceptions.InvalidRequestException as e:
        raise RuntimeError(f"Invalid request: {e}")
    except client.exceptions.InvalidParameterException as e:
        raise RuntimeError(f"Invalid parameter: {e}")
    secret_string = response.get("SecretString")
    if not secret_string:
        raise RuntimeError(f"SecretString is empty for secret")
    return secret_string.encode("utf-8")


PUBLIC_KEY = read_public_key()
PUBLIC_KEY_LAST_READ = time.time()

class TokenClaims(BaseModel):
    # Allow extra unmapped claims from the JWT without raising an error
    model_config = ConfigDict(extra="ignore")

    # Standard JWT registered claims
    sub: str
    exp: int

    # Common custom claims (adjust to match your token payload)
    role = Field(default="user", description="Role of the user")


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> TokenClaims:
    token = credentials.credentials
    user_claims = None
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["ES256"],
            options={"require": ["exp", "sub"]},
        )
        user_claims = TokenClaims.model_validate(payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.InvalidTokenError, ValidationError) as exc:
        # Refresh key if it's been more than an hour since the last read
        if (time.time() - PUBLIC_KEY_LAST_READ) > 3600 :
            global PUBLIC_KEY, PUBLIC_KEY_LAST_READ
            PUBLIC_KEY = read_public_key()
            PUBLIC_KEY_LAST_READ = time.time()
            try:
                payload = jwt.decode(
                    token,
                    PUBLIC_KEY,
                    algorithms=["ES256"],
                    options={"require": ["exp", "sub"]},
                )
                user_claims = TokenClaims.model_validate(payload)
            except (jwt.InvalidTokenError, ValidationError):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token or claims",
                    headers={"WWW-Authenticate": "Bearer"},
                ) from exc
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token or claims",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

    if user_claims['sub']:
        user_claims['sub'] = user_claims['sub'].lower()
    if user_claims['role']:
        user_claims['role'] = user_claims['role'].lower()

    return user_claims

AuthUser = Annotated[TokenClaims, Depends(get_current_user)]
