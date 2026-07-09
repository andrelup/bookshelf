"""Translates domain exceptions into HTTP responses.

Domain services and inbound adapters raise `DomainError` subclasses
directly; this is the single place that maps them to HTTP status codes
and the standard `ApiResponse` envelope, per the hexagonal architecture
rules in `backend/CLAUDE.md`.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from src.adapters.inbound.schemas.common import ApiResponse
from src.domain.exceptions import (
    BookNotFoundError,
    BookValidationError,
    DomainError,
    DuplicateEmailError,
    DuplicateFavouriteBookError,
    DuplicateFavouriteListNameError,
    FavouriteListNotFoundError,
    FavouriteListValidationError,
    ForbiddenError,
    InvalidCredentialsError,
    UnauthorizedError,
)

_STATUS_CODES: dict[type[DomainError], int] = {
    BookNotFoundError: 404,
    UnauthorizedError: 401,
    InvalidCredentialsError: 401,
    ForbiddenError: 403,
    DuplicateEmailError: 409,
    BookValidationError: 422,
    FavouriteListNotFoundError: 404,
    DuplicateFavouriteListNameError: 409,
    DuplicateFavouriteBookError: 409,
    FavouriteListValidationError: 422,
}
_DEFAULT_STATUS_CODE = 500


def register_exception_handlers(app: FastAPI) -> None:
    """Register domain exception handlers on the FastAPI app."""

    @app.exception_handler(DomainError)
    async def _handle_domain_error(_request: Request, exc: DomainError) -> JSONResponse:
        status_code = _STATUS_CODES.get(type(exc), _DEFAULT_STATUS_CODE)
        envelope = ApiResponse[None](success=False, data=None, error=str(exc))
        return JSONResponse(status_code=status_code, content=envelope.model_dump())

    @app.exception_handler(IntegrityError)
    async def _handle_integrity_error(_request: Request, _exc: IntegrityError) -> JSONResponse:
        # A DB-level constraint (typically a UniqueConstraint) rejected the write after
        # an in-memory availability check passed — a race between two concurrent requests.
        # The domain-level Duplicate*Error only catches the non-concurrent case.
        envelope = ApiResponse[None](
            success=False, data=None, error="Conflict: the resource already exists"
        )
        return JSONResponse(status_code=409, content=envelope.model_dump())
