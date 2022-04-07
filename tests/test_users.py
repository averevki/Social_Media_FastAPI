"""Users query tests"""
import pytest
from jose import jwt

from app import schemas
from app.config import settings


def test_user_create(client):
    res = client.post("/users/", json={"email": "testmail@gmail.com",
                                       "password": "test_password123"})
    new_user = schemas.UserResponse(**res.json())  # user response scheme validation
    assert res.status_code == 201
    assert new_user.email == "testmail@gmail.com"


def test_user_login(client, user):
    res = client.post("/login", data={"username": user["email"],
                                      "password": user["password"]})
    assert res.status_code == 200
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.token, settings.jwt_encode_key, algorithms=[settings.jwt_algorithm])
    assert login_res.token_type == "bearer"
    assert payload["user_id"] == user["id"]


@pytest.mark.parametrize("email, password, status_code", [
    ("testmail@gmail.com", "bad_password123", 403),
    ("bad_email@gmail.com", "test_password123", 403),
    ("bad_email@gmail.com", "bad_password123", 403),
    (None, "test_password123", 422),
    ("testmail@gmail.com", None, 422)
])
def test_bad_user_login(client, user, email, password, status_code):
    res = client.post("/login", data={"username": email,
                                      "password": password})
    assert res.status_code == status_code
    if email is None or password is None:
        assert res.json().get("detail")[0].get("msg") == "field required"
    else:
        assert res.json().get("detail") == "invalid credentials"
