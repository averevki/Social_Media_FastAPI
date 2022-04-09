"""Pytest fixtures"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token


SQLALCHEMY_DB_URL = f"{settings.database}://{settings.db_user}:{settings.db_password}" \
                    f"@{settings.host}:{settings.port}/{settings.db_name}_test"
engine = create_engine(SQLALCHEMY_DB_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    """Initializing testing database for possible future manipulations"""
    Base.metadata.drop_all(bind=engine)  # drop all existing tables
    Base.metadata.create_all(bind=engine)  # create tables manually
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session):
    """Initializing of fastapi test client"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db  # override database
    yield TestClient(app)


@pytest.fixture
def user(client):
    """Create user"""
    credentials = {"email": "testmail@gmail.com",
                   "password": "TestPassword123!"}
    res = client.post("/users/", json=credentials)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = credentials["password"]
    return new_user


@pytest.fixture
def user2(client):
    """Create second user"""
    credentials = {"email": "testmail2@gmail.com",
                   "password": "TestPassword123!"}
    res = client.post("/users/", json=credentials)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = credentials["password"]
    return new_user


@pytest.fixture
def token(user):
    """Create access token"""
    return create_access_token(data={"user_id": user["id"]})


@pytest.fixture
def authorized_client(client, token):
    """Authorize user with token"""
    client.headers = {      # appending token to query headers
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def add_test_posts(user, user2, db_session):
    """Add test posts from different users"""
    posts = [
        {
            "title": "My first post",
            "content": "Some stuff",
            "owner_id": user.get("id")
        },
        {
            "title": "My second post",
            "content": "More stuff",
            "owner_id": user.get("id")
        },
        {
            "title": "I love tigers",
            "content": "Tigers are great",
            "owner_id": user.get("id")
        },
        {
            "title": "Second user post",
            "content": "Hi, I'm second user",
            "owner_id": user2.get("id")
        }
    ]
    # add all new posts into the database
    db_session.add_all([models.Post(**post) for post in posts])
    db_session.commit()
    return db_session.query(models.Post).all()
