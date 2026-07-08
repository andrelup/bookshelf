"""Test data factories, shared across unit, integration and API tests."""

from src.domain.models.book import Book

_DEFAULT_BOOK_FIELDS: dict[str, object] = {
    "title": "Clean Architecture",
    "author": "Robert C. Martin",
    "isbn": "978-0134494166",
    "price": 39.99,
    "stock": 5,
    "seller_id": 1,
    "description": "A craftsman's guide to software structure.",
    "category": "Software Engineering",
}


def make_book(**overrides: object) -> Book:
    """Build a valid `Book` for tests, overriding only the fields under test."""
    fields = {**_DEFAULT_BOOK_FIELDS, **overrides}
    return Book(**fields)  # type: ignore[arg-type]
