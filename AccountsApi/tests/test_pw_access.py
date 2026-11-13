from AccountsApi.pw_access import hash_password, verify_password


def test_hash_password_returns_argon2_hash():
    hashed = hash_password("secret")

    assert hashed.startswith("$argon2")
    assert hashed != "secret"


def test_verify_password_returns_true_for_matching_password():
    hashed = hash_password("secret")

    assert verify_password("secret", hashed) is True


def test_verify_password_returns_false_for_wrong_password():
    hashed = hash_password("secret")

    assert verify_password("wrong-secret", hashed) is False