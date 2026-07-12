"""Pydantic request/response schemas for the favourite lists API."""

from pydantic import BaseModel, ConfigDict, Field


class FavouriteListCreate(BaseModel):
    """Payload to create a favourite list. `owner_id` is derived from the caller's token."""

    model_config = ConfigDict(json_schema_extra={"example": {"name": "Summer 2026"}})

    name: str = Field(min_length=1, max_length=120)


class FavouriteListUpdate(BaseModel):
    """Payload to rename an existing favourite list."""

    model_config = ConfigDict(json_schema_extra={"example": {"name": "Summer 2026 reading list"}})

    name: str = Field(min_length=1, max_length=120)


class FavouriteListItemCreate(BaseModel):
    """Payload to add a book to a favourite list."""

    model_config = ConfigDict(json_schema_extra={"example": {"book_id": 1}})

    book_id: int = Field(gt=0, description="Id of the catalog book to add to the list.")


class FavouriteListResponse(BaseModel):
    """Favourite list representation returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int = Field(description="Id of the customer who owns this list.")
    name: str
    book_ids: list[int] = Field(description="Ids of the books collected in this list.")


class FavouriteListCollectionResponse(BaseModel):
    """A collection of a customer's favourite lists."""

    items: list[FavouriteListResponse]
    total: int
