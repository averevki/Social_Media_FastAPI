"""Project settings"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Environment variables"""
    database_url: str = ""

    host: str = "localhost"
    port: str = "5432"
    db_name: str
    db_user: str = "postgres"
    db_password: str

    jwt_encode_key: str
    jwt_algorithm: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
