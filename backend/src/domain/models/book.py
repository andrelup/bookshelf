"""Domain model representing a book listed for sale."""

from dataclasses import dataclass


@dataclass
class Book:
    """A book listed for sale in the catalog.

    Attributes:
        title: Book title.
        author: Book author.
        isbn: International Standard Book Number.
        price: Sale price in the store's currency. Must be greater than zero.
        stock: Number of units available. Must not be negative.
        seller_id: Identifier of the seller who owns this listing.
        description: Free-text description of the book.
        category: Category/genre used for browsing and search.
        id: Unique identifier. `None` for a book not yet persisted.
    """

    title: str
    author: str
    isbn: str
    price: float
    stock: int
    seller_id: int
    description: str
    category: str
    id: int | None = None
