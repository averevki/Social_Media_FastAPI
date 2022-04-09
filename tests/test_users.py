"""Users query tests"""
import pytest
from jose import jwt

from app import schemas
from app.config import settings


@pytest.fixture
def registered_user(client):
    res = client.post("/users/", json={"email": "already@exist.com",
                                       "password": "TestPassword123!"})


def test_user_create(client):
    res = client.post("/users/", json={"email": "testmail@gmail.com",
                                       "password": "TestPassword123!"})
    assert res.status_code == 201
    new_user = schemas.UserResponse(**res.json())  # user response scheme validation
    assert new_user.email == "testmail@gmail.com"


@pytest.mark.parametrize("password", ["qwerty", "pass123", "Qwerty12340", "MyPassword!#$"])
def test_user_create_bad_password(client, password):
    res = client.post("/users/", json={"email": "testmail@gmail.com",
                                       "password": password})
    assert res.status_code == 422       # unprocessable entry
    assert res.json()["detail"] == "password must contain at least 8 characters, one uppercase letter, " \
                                   "one lowercase letter, one number and one special character"


def test_user_create_already_exist(client, registered_user):
    res = client.post("/users/", json={"email": "already@exist.com",
                                       "password": "TestPassword123!"})
    assert res.status_code == 409
    assert res.json()["detail"] == "email already registered (email: already@exist.com)"


def test_user_login(client, user):
    res = client.post("/login", data={"username": user["email"],
                                      "password": user["password"]})
    assert res.status_code == 200
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.token, settings.jwt_encode_key, algorithms=[settings.jwt_algorithm])
    assert login_res.token_type == "bearer"
    assert payload["user_id"] == user["id"]


@pytest.mark.parametrize("email, password, status_code", [
    ("testmail@gmail.com", "BadPassword123!", 403),
    ("bad_email@gmail.com", "TestPassword123!", 403),
    ("bad_email@gmail.com", "BadPassword123!", 403),
    (None, "TestPassword123!", 422),
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
