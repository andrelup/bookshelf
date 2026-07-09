"""Domain model representing a customer's named list of favourite books."""

from dataclasses import dataclass, field


@dataclass
class FavouriteList:
    """A named list of favourite books owned by a customer.

    An aggregate: the list owns its books, referenced by id. British
    spelling (`favourite`) is used consistently across the feature.

    Attributes:
        owner_id: Identifier of the customer who owns this list.
        name: Human-readable list name (e.g. "Summer 2026"), unique per owner.
        book_ids: Ids of the books collected in this list, without duplicates.
        id: Unique identifier. `None` for a list not yet persisted.
    """

    owner_id: int
    name: str
    book_ids: list[int] = field(default_factory=list)
    id: int | None = None
