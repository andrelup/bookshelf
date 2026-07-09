"""Favourite lists endpoints: a customer's named lists of favourite books.

Authorization rules (enforced by `FavouriteListService`, translated to HTTP by
the error_handler middleware):
    - Only customers may use these endpoints (403 for sellers).
    - A customer may only read and edit their own lists (403 otherwise).
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from src.adapters.inbound.middleware.auth import get_current_user
from src.adapters.inbound.schemas.common import ApiResponse
from src.adapters.inbound.schemas.favourite_schemas import (
    FavouriteListCollectionResponse,
    FavouriteListCreate,
    FavouriteListItemCreate,
    FavouriteListResponse,
    FavouriteListUpdate,
)
from src.config.container import get_favourite_list_service
from src.domain.models.favourite import FavouriteList
from src.domain.models.user import User
from src.domain.services.favourite_list_service import FavouriteListService

router = APIRouter(prefix="/favourite-lists", tags=["favourite-lists"])


def _to_response(favourite_list: FavouriteList) -> FavouriteListResponse:
    if favourite_list.id is None:
        raise ValueError("Cannot build a response for a favourite list without an id")
    return FavouriteListResponse(
        id=favourite_list.id,
        owner_id=favourite_list.owner_id,
        name=favourite_list.name,
        book_ids=favourite_list.book_ids,
    )


@router.post("", response_model=ApiResponse[FavouriteListResponse], status_code=201)
async def create_favourite_list(
    payload: FavouriteListCreate,
    favourite_list_service: Annotated[FavouriteListService, Depends(get_favourite_list_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ApiResponse[FavouriteListResponse]:
    """Create a favourite list. Customers only (403 for sellers)."""
    created = await favourite_list_service.create(current_user, payload.name)
    return ApiResponse(success=True, data=_to_response(created), error=None)


@router.get("", response_model=ApiResponse[FavouriteListCollectionResponse])
async def list_favourite_lists(
    favourite_list_service: Annotated[FavouriteListService, Depends(get_favourite_list_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ApiResponse[FavouriteListCollectionResponse]:
    """List the caller's favourite lists. Customers only (403 for sellers)."""
    lists = await favourite_list_service.list_for_owner(current_user)
    data = FavouriteListCollectionResponse(
        items=[_to_response(favourite_list) for favourite_list in lists],
        total=len(lists),
    )
    return ApiResponse(success=True, data=data, error=None)


@router.get("/{list_id}", response_model=ApiResponse[FavouriteListResponse])
async def get_favourite_list(
    list_id: int,
    favourite_list_service: Annotated[FavouriteListService, Depends(get_favourite_list_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ApiResponse[FavouriteListResponse]:
    """Get one favourite list and its books. Only its owner may do this (403 otherwise)."""
    favourite_list = await favourite_list_service.get(current_user, list_id)
    return ApiResponse(success=True, data=_to_response(favourite_list), error=None)


@router.put("/{list_id}", response_model=ApiResponse[FavouriteListResponse])
async def rename_favourite_list(
    list_id: int,
    payload: FavouriteListUpdate,
    favourite_list_service: Annotated[FavouriteListService, Depends(get_favourite_list_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ApiResponse[FavouriteListResponse]:
    """Rename a favourite list. Only its owner may do this (403 otherwise)."""
    updated = await favourite_list_service.rename(current_user, list_id, payload.name)
    return ApiResponse(success=True, data=_to_response(updated), error=None)


@router.delete("/{list_id}", response_model=ApiResponse[None])
async def delete_favourite_list(
    list_id: int,
    favourite_list_service: Annotated[FavouriteListService, Depends(get_favourite_list_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ApiResponse[None]:
    """Delete a favourite list and its items. Only its owner may do this (403 otherwise)."""
    await favourite_list_service.delete(current_user, list_id)
    return ApiResponse(success=True, data=None, error=None)


@router.post("/{list_id}/books", response_model=ApiResponse[FavouriteListResponse], status_code=201)
async def add_book_to_favourite_list(
    list_id: int,
    payload: FavouriteListItemCreate,
    favourite_list_service: Annotated[FavouriteListService, Depends(get_favourite_list_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ApiResponse[FavouriteListResponse]:
    """Add a catalog book to a favourite list. Only its owner may do this (403 otherwise)."""
    updated = await favourite_list_service.add_book(current_user, list_id, payload.book_id)
    return ApiResponse(success=True, data=_to_response(updated), error=None)


@router.delete("/{list_id}/books/{book_id}", response_model=ApiResponse[FavouriteListResponse])
async def remove_book_from_favourite_list(
    list_id: int,
    book_id: int,
    favourite_list_service: Annotated[FavouriteListService, Depends(get_favourite_list_service)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ApiResponse[FavouriteListResponse]:
    """Remove a book from a favourite list. Only its owner may do this (403 otherwise)."""
    updated = await favourite_list_service.remove_book(current_user, list_id, book_id)
    return ApiResponse(success=True, data=_to_response(updated), error=None)
