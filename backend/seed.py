"""Database seed script placeholder.

Actual seeding logic (creating sample books, users, etc.) is deferred
to a later issue once the persistence adapters exist.
"""

import structlog

logger = structlog.get_logger(__name__)


def main() -> None:
    """Entry point for `make seed`. Currently a no-op placeholder."""
    logger.info("seed_skipped", reason="not implemented yet")


if __name__ == "__main__":
    main()
