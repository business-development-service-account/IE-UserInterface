from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./app.db"

    # Application
    app_name: str = "Project Management API"
    app_version: str = "1.0.0"
    debug: bool = True

    # Security (future implementation)
    secret_key: Optional[str] = None
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()