"""Pydantic request/response schemas for the books API."""

from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    """Payload to create a new book. `seller_id` is derived from the caller's token."""

    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    isbn: str = Field(min_length=1, max_length=20)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    description: str = ""
    category: str = Field(min_length=1, max_length=100)


class BookUpdate(BaseModel):
    """Payload to replace an existing book's editable fields."""

    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    isbn: str = Field(min_length=1, max_length=20)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    description: str = ""
    category: str = Field(min_length=1, max_length=100)


class BookResponse(BaseModel):
    """Book representation returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    isbn: str
    price: float
    stock: int
    seller_id: int
    description: str
    category: str


class BookListResponse(BaseModel):
    """A paginated page of books."""

    items: list[BookResponse]
    total: int
    skip: int
    limit: int
