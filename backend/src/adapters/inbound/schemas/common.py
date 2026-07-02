"""Generic API response envelope shared by all endpoints."""

from typing import Generic, TypeVar

from pydantic import BaseModel

DataT = TypeVar("DataT")


class ApiResponse(BaseModel, Generic[DataT]):
    """Standard API response envelope: `{"success", "data", "error"}`."""

    success: bool
    data: DataT | None = None
    error: str | None = None
