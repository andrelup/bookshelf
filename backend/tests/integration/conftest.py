"""Fixtures for repository integration tests.

Spins up a throwaway PostgreSQL container via the Docker CLI so
`SqlAlchemyBookRepository` is exercised against a real database, per the
project's testing conventions (`backend/CLAUDE.md`: "Integración: usar DB
real de test"). If Docker is unavailable, these tests are skipped rather
than failed, so the rest of the suite is unaffected.

The container is fully isolated from any other BookShelf environment: it
uses its own name and host port, distinct from `infra/docker-compose.yml`'s
`bookshelf-postgres` service, so it never collides with a developer's (or
another agent's) locally running stack.
"""

import shutil
import subprocess
import time
from collections.abc import AsyncGenerator, Generator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.adapters.outbound.persistence.sqlalchemy_models import Base

_CONTAINER_NAME = "bookshelf-books-crud-test-db"
_HOST_PORT = 55433
# Throwaway password for an ephemeral, local-only test container torn down
# at the end of the test session — not a real secret.
_TEST_PASSWORD = "test_password"  # noqa: S105
_DATABASE_URL = f"postgresql+asyncpg://postgres:{_TEST_PASSWORD}@localhost:{_HOST_PORT}/postgres"


def _docker_available() -> bool:
    return shutil.which("docker") is not None


def _wait_until_ready(timeout_seconds: float = 30.0) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        probe = subprocess.run(
            ["docker", "exec", _CONTAINER_NAME, "pg_isready", "-U", "postgres"],
            capture_output=True,
            check=False,
        )
        if probe.returncode == 0:
            return True
        time.sleep(0.5)
    return False


@pytest.fixture(scope="session")
def postgres_container() -> Generator[None, None, None]:
    """Start (and tear down) an ephemeral PostgreSQL container for this test session."""
    if not _docker_available():
        pytest.skip("Docker is not available; skipping repository integration tests")

    subprocess.run(["docker", "rm", "-f", _CONTAINER_NAME], capture_output=True, check=False)
    result = subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "--rm",
            "--name",
            _CONTAINER_NAME,
            "-e",
            f"POSTGRES_PASSWORD={_TEST_PASSWORD}",
            "-p",
            f"{_HOST_PORT}:5432",
            "postgres:16-alpine",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        pytest.skip(f"Could not start the test PostgreSQL container: {result.stderr}")

    try:
        if not _wait_until_ready():
            pytest.skip("Test PostgreSQL container did not become ready in time")
        yield
    finally:
        subprocess.run(["docker", "rm", "-f", _CONTAINER_NAME], capture_output=True, check=False)


@pytest.fixture
async def db_session(postgres_container: None) -> AsyncGenerator[AsyncSession, None]:
    """A fresh `AsyncSession` against a clean `books` table for a single test."""
    engine = create_async_engine(_DATABASE_URL)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
    await engine.dispose()
