"""Global fixtures shared by the whole test suite."""

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from src.main import app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """HTTP client bound to the FastAPI app, without a running server."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
