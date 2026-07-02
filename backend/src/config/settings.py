"""Application settings, loaded from environment variables.

Importing this module must never trigger a database connection or
any other side effect.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "BookShelf API"
    environment: str = "development"
    database_url: str = "postgresql+asyncpg://bookshelf:bookshelf@localhost:5432/bookshelf"
    log_level: str = "INFO"


settings = Settings()
