import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "Tourist Discovery API"
    API_V1_STR: str = "/api/v1"

    # CORS origins
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:80",
        "http://127.0.0.1:80",
    ]

    # Database Settings
    # Supports real PostgreSQL or SQLite fallback
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./tourist.db",
        description="Database URL. For async pg use: postgresql+asyncpg://user:pass@host:port/db"
    )

    # Redis Settings
    # Default is localhost redis; if empty, we fall back to a mock/in-memory cache
    REDIS_URL: str = "redis://localhost:6379/0"
    USE_REDIS: bool = True

    # Google Maps SDK Settings
    # If empty, application runs in Mock Mode
    GOOGLE_MAPS_API_KEY: str = ""

    # Rate Limiting
    RATE_LIMIT_LIMIT: int = 60  # requests
    RATE_LIMIT_WINDOW: int = 60  # seconds (1 minute)

    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_URL.startswith("sqlite")

settings = Settings()
