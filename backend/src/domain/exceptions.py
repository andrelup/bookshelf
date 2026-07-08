"""Domain exceptions.

These are translated into HTTP responses by the error_handler
middleware in `adapters/inbound/middleware`. The domain layer never
raises HTTP exceptions directly.
"""


class DomainError(Exception):
    """Base exception for all domain-level errors."""


class BookNotFoundError(DomainError):
    """Raised when a requested book does not exist."""


class UnauthorizedError(DomainError):
    """Raised when an operation is attempted without proper authorization."""
