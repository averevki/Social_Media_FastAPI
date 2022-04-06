"""Users query tests"""
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
