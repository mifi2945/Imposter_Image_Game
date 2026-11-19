import os
from pathlib import Path
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, ValidationError

security = HTTPBearer()
PUBLIC_KEY_PATH = Path(
    os.getenv(
        "JWT_PUBLIC_KEY_PATH",
        "/var/run/secrets/accountsapi-es-public/public-key.pem",
    )
)


class TokenClaims(BaseModel):
    # Allow extra unmapped claims from the JWT without raising an error
    model_config = ConfigDict(extra="ignore")

    # Standard JWT registered claims
    sub: str
    exp: int

    role: str


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> TokenClaims:
    try:
        public_key = PUBLIC_KEY_PATH.read_bytes()
    except OSError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="JWT verification key is unavailable",
        ) from exc

    try:
        payload = jwt.decode(
            credentials.credentials,
            public_key,
            algorithms=["ES256"],
            options={"require": ["exp", "sub", "role"]},
        )
        claims = TokenClaims.model_validate(payload)
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except (jwt.InvalidTokenError, ValidationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or claims",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return TokenClaims(
        sub=claims.sub.lower(),
        exp=claims.exp,
        role=claims.role.lower(),
    )


AuthUser = Annotated[TokenClaims, Depends(get_current_user)]
