"""Connection to database"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# data base url
# for deployment server
if settings.database_url is not None:
    uri = settings.database_url
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DB_URL = uri
else:       # for development
    SQLALCHEMY_DB_URL = f"{settings.database}://{settings.db_user}:{settings.db_password}" \
                        f"@{settings.host}:{settings.port}/{settings.db_name}"
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
