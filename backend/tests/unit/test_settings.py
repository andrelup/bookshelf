"""Unit tests for Settings.database_url composition."""

from typing import Any

import pytest
from pydantic import ValidationError
from src.config.settings import Settings


def make_settings(**overrides: Any) -> Settings:
    """Build Settings isolated from the developer's real .env file."""
    overrides.setdefault("jwt_secret_key", "test-jwt-secret")
    # mypy doesn't know pydantic-settings' _env_file init kwarg.
    return Settings(_env_file=None, **overrides)  # type: ignore[call-arg]


def test_database_url_composed_from_discrete_fields() -> None:
    # Arrange
    settings = make_settings(
        db_host="db.example.com",
        db_port=5433,
        db_username="alice",
        db_password="secret",
        db_name="bookshelf_test",
    )

    # Act
    url = settings.database_url

    # Assert
    assert url == "postgresql+asyncpg://alice:secret@db.example.com:5433/bookshelf_test"


def test_database_url_when_password_has_special_chars_is_url_encoded() -> None:
    # Arrange
    settings = make_settings(
        db_username="alice",
        db_password="p@ss:w/rd+1",
        db_name="bookshelf_test",
    )

    # Act
    url = settings.database_url

    # Assert
    assert "p%40ss%3Aw%2Frd%2B1" in url
    assert "p@ss:w/rd+1" not in url


def test_database_url_defaults_point_to_local_postgres() -> None:
    # Arrange
    settings = make_settings(db_password="secret")

    # Act
    url = settings.database_url

    # Assert
    assert url.startswith("postgresql+asyncpg://")
    assert "@localhost:5432/" in url


def test_settings_when_password_missing_raises_validation_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange — secrets must come from the environment, so instantiating
    # without DB_PASSWORD anywhere must fail loudly.
    monkeypatch.delenv("DB_PASSWORD", raising=False)

    # Act / Assert
    with pytest.raises(ValidationError):
        make_settings()


def test_settings_when_jwt_secret_missing_raises_validation_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange — the JWT signing secret must come from the environment too.
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    # Act / Assert
    with pytest.raises(ValidationError):
        Settings(_env_file=None, db_password="secret")  # type: ignore[call-arg]


def test_settings_jwt_defaults() -> None:
    # Arrange / Act
    settings = make_settings(db_password="secret")

    # Assert
    assert settings.jwt_algorithm == "HS256"
    assert settings.jwt_access_token_expires_minutes == 60
