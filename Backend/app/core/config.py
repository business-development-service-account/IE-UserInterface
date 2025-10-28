from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./app.db"

    # Application
    app_name: str = "IE UserInterface API"
    app_version: str = "1.0.0"
    debug: bool = True

    # Security
    secret_key: str = "ie-userinterface-secret-key-change-in-production-2025"
    access_token_expire_minutes: int = 15

    # CORS
    cors_origins: List[str] = [
        "http://localhost:3002",
        "http://localhost:3000",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:3000"
    ]

    class Config:
        env_file = ".env"


settings = Settings()