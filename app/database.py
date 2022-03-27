"""Connection to database"""
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

database = getenv("DATABASE")
username = getenv("DB_USER")
password = getenv("DB_PASSWORD")
port = getenv("HOST")
db_name = getenv("DB_NAME")

SQLALCHEMY_DB_URL = f"{database}://{username}:{password}@{port}/{db_name}"
engine = create_engine(SQLALCHEMY_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
