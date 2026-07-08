"""Application settings, loaded from environment variables.

Importing this module must never trigger a database connection or
any other side effect.
"""

from urllib.parse import quote_plus

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
    db_host: str = "localhost"
    db_port: int = 5432
    db_username: str = "bookshelf"
    # Required on purpose: secrets must come from the environment, never code.
    db_password: str
    db_name: str = "bookshelf"
    log_level: str = "INFO"

    @property
    def database_url(self) -> str:
        """Async SQLAlchemy URL built from the discrete DB_* variables."""
        return (
            f"postgresql+asyncpg://{self.db_username}:{quote_plus(self.db_password)}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


# mypy can't know that the required db_password arrives via .env at runtime.
settings = Settings()  # type: ignore[call-arg]
