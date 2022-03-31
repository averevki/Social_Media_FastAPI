"""Connection to database"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

database = settings.database
username = settings.db_user
password = settings.db_password
port = settings.host
db_name = settings.db_name

SQLALCHEMY_DB_URL = f"{database}://{username}:{password}@{port}/{db_name}"
engine = create_engine(SQLALCHEMY_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Virtual database instance"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
