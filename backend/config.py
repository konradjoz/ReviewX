import secrets
from typing import List

from pydantic import BaseSettings, AnyHttpUrl


class BasicSettings(BaseSettings):
    APPLICATION_NAME: str = "FARM Starter"
    AUTHOR: str = "KonradJoz"
    VERSION: str = "v1"

    API_PATH: str = f"/api/{VERSION}/"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8080", "http://localhost:3000"]

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class MongoDBSettings(BaseSettings):
    DB_URL: str = "mongodb+srv://root:eauTEEvJzlzgHcmE@reviewapi-cluster.xb7wp.mongodb.net/ReviewX?retryWrites=true&w=majority"
    DB_NAME: str = "ReviewX"


class Settings(BasicSettings, ServerSettings, MongoDBSettings):
    pass


settings = Settings()
