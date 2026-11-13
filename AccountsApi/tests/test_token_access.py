import datetime
import hashlib

import jwt

from AccountsApi.token_access import ALG, PRIVATE_KEY, Token

def test_get_public_key_returns_configured_public_key():
    assert Token.get_public_key()


def test_create_access_token_contains_user_role_and_future_expiration():
    token = Token.create_access_token("alice", "admin")

    claims = jwt.decode(token, options={"verify_signature": False})

    assert claims["sub"] == "alice"
    assert claims["role"] == "admin"
    assert datetime.datetime.fromtimestamp(claims["exp"], datetime.timezone.utc) > datetime.datetime.now(
        datetime.timezone.utc
    )


def test_verify_access_token_returns_claims_for_valid_token():
    token = Token.create_access_token("alice", "user")

    assert Token.verify_access_token(token) == jwt.decode(
        token, Token.get_public_key(), algorithms=[ALG]
    )


def test_verify_access_token_returns_none_for_tampered_token():
    token = Token.create_access_token("alice", "user")
    tampered_token = token[:-1] + ("a" if token[-1] != "a" else "b")

    assert Token.verify_access_token(tampered_token) is None


def test_verify_access_token_returns_none_for_expired_token():
    expired_claims = {
        "sub": "alice",
        "role": "user",
        "exp": (
            datetime.datetime.now(datetime.timezone.utc)
            - datetime.timedelta(minutes=1)
        ).isoformat(),
    }
    token = jwt.encode(expired_claims, PRIVATE_KEY, algorithm=ALG)

    assert Token.verify_access_token(token) is None


def test_verify_access_token_returns_none_when_required_claim_is_missing():
    claims = {
        "sub": "alice",
        "exp": (
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(minutes=15)
        ).isoformat(),
    }
    token = jwt.encode(claims, PRIVATE_KEY, algorithm=ALG)

    assert Token.verify_access_token(token) is None


def test_gen_tokens_returns_verifiable_access_and_hashed_refresh_tokens():
    tokens = Token.gen_tokens("alice", "user")

    assert set(tokens) == {
        "access_token",
        "raw_refresh_token",
        "hash_refresh_token",
    }
    assert Token.verify_access_token(tokens["access_token"]) == {
        "sub": "alice",
        "role": "user",
        "exp": jwt.decode(
            tokens["access_token"], options={"verify_signature": False}
        )["exp"],
    }
    assert tokens["hash_refresh_token"] == hashlib.sha256(
        tokens["raw_refresh_token"].encode()
    ).hexdigest()


def test_hash_token_returns_sha256_hex_digest():
    token = "refresh-token"

    assert Token.hash_token(token) == hashlib.sha256(token.encode()).hexdigest()
