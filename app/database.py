from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database = "postgresql"
username = "postgres"
password = "123321"
port = "localhost"
db_name = "social_media_db"

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
