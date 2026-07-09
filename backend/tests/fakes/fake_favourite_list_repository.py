"""In-memory fake implementing the `FavouriteListRepository` port, for fast tests.

Used by unit tests (domain service, mocked ports — no DB/I/O) and by API
tests (dependency-overriding the outbound port so router tests exercise
wiring, validation and error translation without a real database).
"""

from dataclasses import replace

from src.domain.models.favourite import FavouriteList


class FakeFavouriteListRepository:
    """An in-memory `FavouriteListRepository` backed by a plain dict, for tests."""

    def __init__(self, favourite_lists: list[FavouriteList] | None = None) -> None:
        self._lists: dict[int, FavouriteList] = {}
        self._next_id = 1
        for favourite_list in favourite_lists or []:
            self._add(favourite_list)

    def _add(self, favourite_list: FavouriteList) -> FavouriteList:
        list_id = favourite_list.id if favourite_list.id is not None else self._next_id
        stored = replace(favourite_list, id=list_id, book_ids=list(favourite_list.book_ids))
        self._lists[list_id] = stored
        self._next_id = max(self._next_id, list_id + 1)
        return replace(stored, book_ids=list(stored.book_ids))

    async def find_by_id(self, list_id: int) -> FavouriteList | None:
        stored = self._lists.get(list_id)
        return replace(stored, book_ids=list(stored.book_ids)) if stored is not None else None

    async def find_all_by_owner(self, owner_id: int) -> list[FavouriteList]:
        ordered = sorted(self._lists.values(), key=lambda fl: fl.id or 0)
        return [
            replace(fl, book_ids=list(fl.book_ids)) for fl in ordered if fl.owner_id == owner_id
        ]

    async def find_by_owner_and_name(self, owner_id: int, name: str) -> FavouriteList | None:
        for favourite_list in sorted(self._lists.values(), key=lambda fl: fl.id or 0):
            if favourite_list.owner_id == owner_id and favourite_list.name == name:
                return replace(favourite_list, book_ids=list(favourite_list.book_ids))
        return None

    async def save(self, favourite_list: FavouriteList) -> FavouriteList:
        return self._add(favourite_list)

    async def delete(self, list_id: int) -> None:
        self._lists.pop(list_id, None)
