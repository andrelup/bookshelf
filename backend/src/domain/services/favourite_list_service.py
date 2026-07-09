"""Favourite list use cases: create, list, get, rename, delete and manage books.

Only customers may manage favourite lists, and each customer may only reach
their own lists. Both rules are enforced here (not in a middleware) and
translated to HTTP 403 by the error_handler middleware, mirroring the pattern
established by `BookService`.
"""

from src.domain.exceptions import (
    BookNotFoundError,
    DuplicateFavouriteBookError,
    DuplicateFavouriteListNameError,
    FavouriteListNotFoundError,
    FavouriteListValidationError,
    ForbiddenError,
)
from src.domain.models.favourite import FavouriteList
from src.domain.models.user import User, UserRole
from src.domain.ports.repositories import BookRepository, FavouriteListRepository


class FavouriteListService:
    """Business rules for customers' named lists of favourite books.

    Every operation requires the "customer" role and ownership of the target
    list. Adding a book validates that the book exists in the catalog.
    """

    def __init__(
        self,
        favourite_list_repository: FavouriteListRepository,
        book_repository: BookRepository,
    ) -> None:
        self._favourite_list_repository = favourite_list_repository
        self._book_repository = book_repository

    async def create(self, user: User, name: str) -> FavouriteList:
        """Create a new, empty favourite list owned by `user`.

        Raises:
            ForbiddenError: if `user` is not a customer.
            FavouriteListValidationError: if `name` is blank.
            DuplicateFavouriteListNameError: if the owner already has that name.
        """
        owner_id = self._ensure_customer(user)
        clean_name = self._validate_name(name)
        await self._ensure_name_available(owner_id, clean_name)
        candidate = FavouriteList(owner_id=owner_id, name=clean_name, book_ids=[])
        return await self._favourite_list_repository.save(candidate)

    async def list_for_owner(self, user: User) -> list[FavouriteList]:
        """Return every favourite list owned by `user`.

        Raises:
            ForbiddenError: if `user` is not a customer.
        """
        owner_id = self._ensure_customer(user)
        return await self._favourite_list_repository.find_all_by_owner(owner_id)

    async def get(self, user: User, list_id: int) -> FavouriteList:
        """Return a single favourite list owned by `user`.

        Raises:
            ForbiddenError: if `user` is not a customer, or not the list's owner.
            FavouriteListNotFoundError: if no list exists with `list_id`.
        """
        self._ensure_customer(user)
        favourite_list = await self._get_or_raise(list_id)
        self._ensure_owner(user, favourite_list)
        return favourite_list

    async def rename(self, user: User, list_id: int, name: str) -> FavouriteList:
        """Rename an existing favourite list owned by `user`.

        Raises:
            ForbiddenError: if `user` is not a customer, or not the list's owner.
            FavouriteListNotFoundError: if no list exists with `list_id`.
            FavouriteListValidationError: if `name` is blank.
            DuplicateFavouriteListNameError: if the owner already has that name.
        """
        owner_id = self._ensure_customer(user)
        favourite_list = await self._get_or_raise(list_id)
        self._ensure_owner(user, favourite_list)
        clean_name = self._validate_name(name)
        if clean_name != favourite_list.name:
            await self._ensure_name_available(owner_id, clean_name)
        favourite_list.name = clean_name
        return await self._favourite_list_repository.save(favourite_list)

    async def delete(self, user: User, list_id: int) -> None:
        """Delete a favourite list (and its items) owned by `user`.

        Raises:
            ForbiddenError: if `user` is not a customer, or not the list's owner.
            FavouriteListNotFoundError: if no list exists with `list_id`.
        """
        self._ensure_customer(user)
        favourite_list = await self._get_or_raise(list_id)
        self._ensure_owner(user, favourite_list)
        await self._favourite_list_repository.delete(list_id)

    async def add_book(self, user: User, list_id: int, book_id: int) -> FavouriteList:
        """Add a catalog book to a favourite list owned by `user`.

        Raises:
            ForbiddenError: if `user` is not a customer, or not the list's owner.
            FavouriteListNotFoundError: if no list exists with `list_id`.
            BookNotFoundError: if no book exists with `book_id`.
            DuplicateFavouriteBookError: if the book is already in the list.
        """
        self._ensure_customer(user)
        favourite_list = await self._get_or_raise(list_id)
        self._ensure_owner(user, favourite_list)
        if await self._book_repository.find_by_id(book_id) is None:
            raise BookNotFoundError(f"Book {book_id} not found")
        if book_id in favourite_list.book_ids:
            raise DuplicateFavouriteBookError(
                f"Book {book_id} is already in favourite list {list_id}"
            )
        favourite_list.book_ids.append(book_id)
        return await self._favourite_list_repository.save(favourite_list)

    async def remove_book(self, user: User, list_id: int, book_id: int) -> FavouriteList:
        """Remove a book from a favourite list owned by `user`.

        Removing a book that is not in the list is a no-op, not an error.

        Raises:
            ForbiddenError: if `user` is not a customer, or not the list's owner.
            FavouriteListNotFoundError: if no list exists with `list_id`.
        """
        self._ensure_customer(user)
        favourite_list = await self._get_or_raise(list_id)
        self._ensure_owner(user, favourite_list)
        if book_id in favourite_list.book_ids:
            favourite_list.book_ids.remove(book_id)
            return await self._favourite_list_repository.save(favourite_list)
        return favourite_list

    async def _get_or_raise(self, list_id: int) -> FavouriteList:
        favourite_list = await self._favourite_list_repository.find_by_id(list_id)
        if favourite_list is None:
            raise FavouriteListNotFoundError(f"Favourite list {list_id} not found")
        return favourite_list

    async def _ensure_name_available(self, owner_id: int, name: str) -> None:
        existing = await self._favourite_list_repository.find_by_owner_and_name(owner_id, name)
        if existing is not None:
            raise DuplicateFavouriteListNameError(f"A favourite list named {name!r} already exists")

    @staticmethod
    def _ensure_customer(user: User) -> int:
        """Check `user` has the "customer" role and return their (persisted) id."""
        if user.role != UserRole.CUSTOMER:
            raise ForbiddenError("Only customers can manage favourite lists")
        if user.id is None:
            # Defensive: an authenticated customer is always a persisted user.
            raise ForbiddenError("Only customers can manage favourite lists")
        return user.id

    @staticmethod
    def _ensure_owner(user: User, favourite_list: FavouriteList) -> None:
        if favourite_list.owner_id != user.id:
            raise ForbiddenError("Customers can only manage their own favourite lists")

    @staticmethod
    def _validate_name(name: str) -> str:
        clean_name = name.strip()
        if not clean_name:
            raise FavouriteListValidationError("Favourite list name cannot be empty")
        return clean_name
