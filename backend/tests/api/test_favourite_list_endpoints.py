"""API tests for the favourite lists router: httpx.AsyncClient against the app.

Covers status codes, the `{"success", "data", "error"}` envelope and
authorization (401 unauthenticated, 403 for sellers, 404 for cross-customer
access, 409 error translation).
"""

from collections.abc import Callable

import httpx
from src.domain.models.user import User
from src.domain.services.book_service import BookService
from src.domain.services.favourite_list_service import FavouriteListService

from tests.factories import make_book


async def _create_list(client: httpx.AsyncClient, name: str = "Summer 2026") -> dict[str, object]:
    response = await client.post("/favourite-lists", json={"name": name})
    assert response.status_code == 201
    data: dict[str, object] = response.json()["data"]
    return data


async def test_create_list_when_customer_returns_201(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    customer_user: User,
) -> None:
    # Arrange
    authenticated_as(customer_user)

    # Act
    response = await client.post("/favourite-lists", json={"name": "Summer 2026"})

    # Assert
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["error"] is None
    assert body["data"]["name"] == "Summer 2026"
    assert body["data"]["owner_id"] == customer_user.id
    assert body["data"]["book_ids"] == []


async def test_create_list_when_seller_returns_403(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    seller_user: User,
) -> None:
    # Arrange
    authenticated_as(seller_user)

    # Act
    response = await client.post("/favourite-lists", json={"name": "Summer 2026"})

    # Assert
    assert response.status_code == 403
    body = response.json()
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"] is not None


async def test_create_list_when_no_credentials_returns_401(client: httpx.AsyncClient) -> None:
    # Act — `authenticated_as` was never called, so the real provisional
    # `get_current_user` dependency runs against a request with no token.
    response = await client.post("/favourite-lists", json={"name": "Summer 2026"})

    # Assert
    assert response.status_code == 401


async def test_create_list_when_name_blank_returns_422(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    customer_user: User,
) -> None:
    # Arrange
    authenticated_as(customer_user)

    # Act
    response = await client.post("/favourite-lists", json={"name": ""})

    # Assert
    assert response.status_code == 422


async def test_create_list_when_name_duplicated_returns_409(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    customer_user: User,
) -> None:
    # Arrange
    authenticated_as(customer_user)
    await _create_list(client)

    # Act
    response = await client.post("/favourite-lists", json={"name": "Summer 2026"})

    # Assert
    assert response.status_code == 409


async def test_list_lists_returns_only_own_lists(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    customer_user: User,
    other_customer_user: User,
) -> None:
    # Arrange
    authenticated_as(other_customer_user)
    await _create_list(client, name="Theirs")
    authenticated_as(customer_user)
    await _create_list(client, name="Mine")

    # Act
    response = await client.get("/favourite-lists")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["total"] == 1
    assert body["data"]["items"][0]["name"] == "Mine"


async def test_get_list_when_owner_returns_200(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    customer_user: User,
) -> None:
    # Arrange
    authenticated_as(customer_user)
    created = await _create_list(client)

    # Act
    response = await client.get(f"/favourite-lists/{created['id']}")

    # Assert
    assert response.status_code == 200
    assert response.json()["data"]["id"] == created["id"]


async def test_get_list_when_missing_returns_404(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    customer_user: User,
) -> None:
    # Arrange
    authenticated_as(customer_user)

    # Act
    response = await client.get("/favourite-lists/999")

    # Assert
    assert response.status_code == 404
    assert response.json()["success"] is False


async def test_get_list_when_another_customers_returns_404(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    customer_user: User,
    other_customer_user: User,
) -> None:
    # Arrange
    authenticated_as(customer_user)
    created = await _create_list(client)
    authenticated_as(other_customer_user)

    # Act
    response = await client.get(f"/favourite-lists/{created['id']}")

    # Assert
    assert response.status_code == 404


async def test_rename_list_when_owner_returns_200(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    customer_user: User,
) -> None:
    # Arrange
    authenticated_as(customer_user)
    created = await _create_list(client)

    # Act
    response = await client.put(f"/favourite-lists/{created['id']}", json={"name": "Beach reads"})

    # Assert
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Beach reads"


async def test_delete_list_when_owner_returns_200_and_removes_it(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    customer_user: User,
) -> None:
    # Arrange
    authenticated_as(customer_user)
    created = await _create_list(client)

    # Act
    response = await client.delete(f"/favourite-lists/{created['id']}")

    # Assert
    assert response.status_code == 200
    assert response.json()["success"] is True
    follow_up = await client.get(f"/favourite-lists/{created['id']}")
    assert follow_up.status_code == 404


async def test_add_book_when_owner_returns_201_with_book(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    customer_user: User,
    seller_user: User,
    book_service: BookService,
) -> None:
    # Arrange
    book = await book_service.create(seller_user, make_book())
    assert book.id is not None
    authenticated_as(customer_user)
    created = await _create_list(client)

    # Act
    response = await client.post(
        f"/favourite-lists/{created['id']}/books", json={"book_id": book.id}
    )

    # Assert
    assert response.status_code == 201
    assert response.json()["data"]["book_ids"] == [book.id]


async def test_add_book_when_book_missing_returns_404(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    customer_user: User,
) -> None:
    # Arrange
    authenticated_as(customer_user)
    created = await _create_list(client)

    # Act
    response = await client.post(f"/favourite-lists/{created['id']}/books", json={"book_id": 999})

    # Assert
    assert response.status_code == 404


async def test_add_book_when_duplicate_returns_409(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    customer_user: User,
    seller_user: User,
    book_service: BookService,
) -> None:
    # Arrange
    book = await book_service.create(seller_user, make_book())
    assert book.id is not None
    authenticated_as(customer_user)
    created = await _create_list(client)
    await client.post(f"/favourite-lists/{created['id']}/books", json={"book_id": book.id})

    # Act
    response = await client.post(
        f"/favourite-lists/{created['id']}/books", json={"book_id": book.id}
    )

    # Assert
    assert response.status_code == 409


async def test_remove_book_when_owner_returns_200_and_removes_it(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    customer_user: User,
    seller_user: User,
    book_service: BookService,
) -> None:
    # Arrange
    book = await book_service.create(seller_user, make_book())
    assert book.id is not None
    authenticated_as(customer_user)
    created = await _create_list(client)
    await client.post(f"/favourite-lists/{created['id']}/books", json={"book_id": book.id})

    # Act
    response = await client.delete(f"/favourite-lists/{created['id']}/books/{book.id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["data"]["book_ids"] == []


async def test_add_book_when_seller_returns_403(
    client: httpx.AsyncClient,
    authenticated_as: Callable[[User], None],
    seller_user: User,
    favourite_list_service: FavouriteListService,
    customer_user: User,
) -> None:
    # Arrange — a customer owns the list, then a seller attempts to touch it.
    created = await favourite_list_service.create(customer_user, "Summer 2026")
    assert created.id is not None
    authenticated_as(seller_user)

    # Act
    response = await client.post(f"/favourite-lists/{created.id}/books", json={"book_id": 1})

    # Assert
    assert response.status_code == 403
