"""Inventory database helpers."""

from app.db import Base, engine


def init_inventory() -> None:
    """Create inventory tables within the shared database."""
    Base.metadata.create_all(bind=engine)
