import pytest

from app import schemas
from .db_setup import client, db_session


def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json().get("message") == "Hello :)"


def test_user_create(client):
    res = client.post("/users/", json={"email": "testmail@gmail.com",
                                       "password": "test_password123"})
    new_user = schemas.UserResponse(**res.json())  # user response scheme validation
    assert res.status_code == 201
    assert new_user.email == "testmail@gmail.com"
