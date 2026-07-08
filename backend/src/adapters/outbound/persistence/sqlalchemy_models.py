"""SQLAlchemy ORM models — kept separate from domain models.

Domain models (`src/domain/models/`) are plain dataclasses; these are the
persistence-specific counterparts, mapped to/from the domain via the
mapper functions in the matching `*_repository.py` module.
"""

from sqlalchemy import Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""


class UserORM(Base):
    """`users` table."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)


class BookORM(Base):
    """ORM mapping for the `books` table.

    `seller_id` is a logical reference to `users.id`. No physical foreign
    key constraint is declared yet — see the accompanying Alembic
    migration's docstring for the plan to add it once both migrations
    (users, books) are chained in the same history.
    """

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    isbn: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False, default=0)
    seller_id: Mapped[int] = mapped_column(nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
