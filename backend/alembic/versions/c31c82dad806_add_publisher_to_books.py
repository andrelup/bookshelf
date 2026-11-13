"""add publisher to books

Revision ID: c31c82dad806
Revises: f16ee8143e9d
Create Date: 2026-11-13 00:35:20.420522

Adds an optional `publisher` column to `books` holding the book's publishing
house (editorial). NULL means unknown, so existing rows stay valid without a
backfill and the column needs no `server_default`.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c31c82dad806"
down_revision: str | None = "f16ee8143e9d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("books", sa.Column("publisher", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("books", "publisher")
