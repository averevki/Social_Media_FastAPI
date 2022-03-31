"""Project settings"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Environment variables"""
    host: str = "localhost"
    database: str = "postgresql"
    db_name: str
    db_user: str = "postgres"
    db_password: str

    jwt_encode_key: str
    jwt_algorithm: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()