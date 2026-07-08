"""Fixtures for API tests: httpx.AsyncClient wired to the FastAPI app.

The outbound `BookRepository` port is faked out via FastAPI dependency
overrides, so these tests exercise router wiring, request/response
validation and error-to-HTTP translation without needing a real database.
`get_current_user` is left un-overridden by default, so tests that don't
call `authenticated_as` exercise the real provisional JWT dependency
(e.g. to verify 401 on missing credentials).
"""

from collections.abc import AsyncGenerator, Callable

import httpx
import pytest
from src.adapters.inbound.middleware.auth import get_current_user
from src.config.container import get_book_service
from src.domain.models.user import User
from src.domain.services.book_service import BookService
from src.main import app

from tests.fakes.fake_book_repository import FakeBookRepository


@pytest.fixture
def book_service() -> BookService:
    """A `BookService` backed by an isolated in-memory fake repository per test."""
    return BookService(FakeBookRepository())


@pytest.fixture
def authenticated_as() -> Callable[[User], None]:
    """Return a function that overrides `get_current_user` for the app under test."""

    def _authenticate(user: User) -> None:
        app.dependency_overrides[get_current_user] = lambda: user

    return _authenticate


@pytest.fixture
async def client(book_service: BookService) -> AsyncGenerator[httpx.AsyncClient, None]:
    """An `httpx.AsyncClient` wired to the app, with the book service faked out."""
    app.dependency_overrides[get_book_service] = lambda: book_service
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
    app.dependency_overrides.clear()
