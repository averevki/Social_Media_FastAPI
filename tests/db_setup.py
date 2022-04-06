import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.config import settings
from app.database import get_db, Base

SQLALCHEMY_DB_URL = f"{settings.database}://{settings.db_user}:{settings.db_password}" \
                    f"@{settings.host}:{settings.port}/{settings.db_name}_test"
engine = create_engine(SQLALCHEMY_DB_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db_session():
    """Initializing testing database for possible future manipulations"""
    Base.metadata.drop_all(bind=engine)  # drop all existing tables
    Base.metadata.create_all(bind=engine)  # create tables manually
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(db_session):
    """Initializing of fastapi test client"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db  # override database
    yield TestClient(app)

