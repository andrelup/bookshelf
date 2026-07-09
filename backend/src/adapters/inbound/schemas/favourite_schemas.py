"""Pydantic request/response schemas for the favourite lists API."""

from pydantic import BaseModel, ConfigDict, Field


class FavouriteListCreate(BaseModel):
    """Payload to create a favourite list. `owner_id` is derived from the caller's token."""

    name: str = Field(min_length=1, max_length=120)


class FavouriteListUpdate(BaseModel):
    """Payload to rename an existing favourite list."""

    name: str = Field(min_length=1, max_length=120)


class FavouriteListItemCreate(BaseModel):
    """Payload to add a book to a favourite list."""

    book_id: int = Field(gt=0)


class FavouriteListResponse(BaseModel):
    """Favourite list representation returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    name: str
    book_ids: list[int]


class FavouriteListCollectionResponse(BaseModel):
    """A collection of a customer's favourite lists."""

    items: list[FavouriteListResponse]
    total: int
