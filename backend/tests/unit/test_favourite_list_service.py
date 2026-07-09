"""Unit tests for `FavouriteListService`, using in-memory fakes (no DB)."""

import pytest
from src.domain.exceptions import (
    BookNotFoundError,
    DuplicateFavouriteBookError,
    DuplicateFavouriteListNameError,
    FavouriteListNotFoundError,
    FavouriteListValidationError,
    ForbiddenError,
)
from src.domain.models.user import User
from src.domain.services.favourite_list_service import FavouriteListService

from tests.factories import make_book
from tests.fakes.fake_book_repository import FakeBookRepository
from tests.fakes.fake_favourite_list_repository import FakeFavouriteListRepository


@pytest.fixture
def book_repository() -> FakeBookRepository:
    """A book repository pre-seeded with one book (id=1) for add-book tests."""
    return FakeBookRepository([make_book()])


@pytest.fixture
def sut(book_repository: FakeBookRepository) -> FavouriteListService:
    return FavouriteListService(FakeFavouriteListRepository(), book_repository)


async def test_create_when_customer_returns_saved_list_owned_by_customer(
    sut: FavouriteListService, customer_user: User
) -> None:
    # Act
    created = await sut.create(customer_user, "Summer 2026")

    # Assert
    assert created.id is not None
    assert created.owner_id == customer_user.id
    assert created.name == "Summer 2026"
    assert created.book_ids == []


async def test_create_strips_whitespace_from_name(
    sut: FavouriteListService, customer_user: User
) -> None:
    # Act
    created = await sut.create(customer_user, "  Gifts  ")

    # Assert
    assert created.name == "Gifts"


async def test_create_when_seller_raises_forbidden(
    sut: FavouriteListService, seller_user: User
) -> None:
    # Act / Assert
    with pytest.raises(ForbiddenError):
        await sut.create(seller_user, "Summer 2026")


@pytest.mark.parametrize("name", ["", "   "])
async def test_create_when_name_blank_raises_validation_error(
    sut: FavouriteListService, customer_user: User, name: str
) -> None:
    # Act / Assert
    with pytest.raises(FavouriteListValidationError):
        await sut.create(customer_user, name)


async def test_create_when_name_duplicated_for_owner_raises(
    sut: FavouriteListService, customer_user: User
) -> None:
    # Arrange
    await sut.create(customer_user, "Summer 2026")

    # Act / Assert
    with pytest.raises(DuplicateFavouriteListNameError):
        await sut.create(customer_user, "Summer 2026")


async def test_list_for_owner_returns_only_own_lists(
    sut: FavouriteListService, customer_user: User, other_customer_user: User
) -> None:
    # Arrange
    await sut.create(customer_user, "Mine A")
    await sut.create(customer_user, "Mine B")
    await sut.create(other_customer_user, "Theirs")

    # Act
    lists = await sut.list_for_owner(customer_user)

    # Assert
    assert {favourite_list.name for favourite_list in lists} == {"Mine A", "Mine B"}


async def test_list_for_owner_when_seller_raises_forbidden(
    sut: FavouriteListService, seller_user: User
) -> None:
    # Act / Assert
    with pytest.raises(ForbiddenError):
        await sut.list_for_owner(seller_user)


async def test_get_when_owner_returns_list(sut: FavouriteListService, customer_user: User) -> None:
    # Arrange
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None

    # Act
    fetched = await sut.get(customer_user, created.id)

    # Assert
    assert fetched.id == created.id


async def test_get_when_missing_raises_not_found(
    sut: FavouriteListService, customer_user: User
) -> None:
    # Act / Assert
    with pytest.raises(FavouriteListNotFoundError):
        await sut.get(customer_user, 999)


async def test_get_when_another_customers_list_raises_not_found(
    sut: FavouriteListService, customer_user: User, other_customer_user: User
) -> None:
    # Arrange
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None

    # Act / Assert
    with pytest.raises(FavouriteListNotFoundError):
        await sut.get(other_customer_user, created.id)


async def test_rename_when_owner_changes_name(
    sut: FavouriteListService, customer_user: User
) -> None:
    # Arrange
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None

    # Act
    renamed = await sut.rename(customer_user, created.id, "Beach reads")

    # Assert
    assert renamed.id == created.id
    assert renamed.name == "Beach reads"


async def test_rename_to_same_name_is_allowed(
    sut: FavouriteListService, customer_user: User
) -> None:
    # Arrange
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None

    # Act
    renamed = await sut.rename(customer_user, created.id, "Summer 2026")

    # Assert
    assert renamed.name == "Summer 2026"


async def test_rename_to_another_existing_name_raises_duplicate(
    sut: FavouriteListService, customer_user: User
) -> None:
    # Arrange
    await sut.create(customer_user, "Gifts")
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None

    # Act / Assert
    with pytest.raises(DuplicateFavouriteListNameError):
        await sut.rename(customer_user, created.id, "Gifts")


async def test_rename_when_another_customers_list_raises_not_found(
    sut: FavouriteListService, customer_user: User, other_customer_user: User
) -> None:
    # Arrange
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None

    # Act / Assert
    with pytest.raises(FavouriteListNotFoundError):
        await sut.rename(other_customer_user, created.id, "Hijacked")


async def test_delete_when_owner_removes_list(
    sut: FavouriteListService, customer_user: User
) -> None:
    # Arrange
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None

    # Act
    await sut.delete(customer_user, created.id)

    # Assert
    with pytest.raises(FavouriteListNotFoundError):
        await sut.get(customer_user, created.id)


async def test_delete_when_another_customers_list_raises_not_found(
    sut: FavouriteListService, customer_user: User, other_customer_user: User
) -> None:
    # Arrange
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None

    # Act / Assert
    with pytest.raises(FavouriteListNotFoundError):
        await sut.delete(other_customer_user, created.id)


async def test_add_book_when_book_exists_appends_it(
    sut: FavouriteListService, customer_user: User
) -> None:
    # Arrange
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None

    # Act
    updated = await sut.add_book(customer_user, created.id, 1)

    # Assert
    assert updated.book_ids == [1]


async def test_add_book_when_book_missing_raises_not_found(
    sut: FavouriteListService, customer_user: User
) -> None:
    # Arrange
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None

    # Act / Assert
    with pytest.raises(BookNotFoundError):
        await sut.add_book(customer_user, created.id, 999)


async def test_add_book_when_already_present_raises_duplicate(
    sut: FavouriteListService, customer_user: User
) -> None:
    # Arrange
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None
    await sut.add_book(customer_user, created.id, 1)

    # Act / Assert
    with pytest.raises(DuplicateFavouriteBookError):
        await sut.add_book(customer_user, created.id, 1)


async def test_add_book_when_another_customers_list_raises_not_found(
    sut: FavouriteListService, customer_user: User, other_customer_user: User
) -> None:
    # Arrange
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None

    # Act / Assert
    with pytest.raises(FavouriteListNotFoundError):
        await sut.add_book(other_customer_user, created.id, 1)


async def test_remove_book_when_present_removes_it(
    sut: FavouriteListService, customer_user: User
) -> None:
    # Arrange
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None
    await sut.add_book(customer_user, created.id, 1)

    # Act
    updated = await sut.remove_book(customer_user, created.id, 1)

    # Assert
    assert updated.book_ids == []


async def test_remove_book_when_absent_is_noop(
    sut: FavouriteListService, customer_user: User
) -> None:
    # Arrange
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None

    # Act — removing a book that is not in the list is a no-op, not an error.
    updated = await sut.remove_book(customer_user, created.id, 1)

    # Assert
    assert updated.book_ids == []


async def test_remove_book_when_another_customers_list_raises_not_found(
    sut: FavouriteListService, customer_user: User, other_customer_user: User
) -> None:
    # Arrange
    created = await sut.create(customer_user, "Summer 2026")
    assert created.id is not None

    # Act / Assert
    with pytest.raises(FavouriteListNotFoundError):
        await sut.remove_book(other_customer_user, created.id, 1)
