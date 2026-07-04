import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read database URL from environment; default to a local SQLite file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")

Base = declarative_base()
engine = None
SessionLocal = None
_current_database_url = None


def _initialize_engine() -> None:
    global engine, SessionLocal, _current_database_url
    current_url = os.getenv("DATABASE_URL", "sqlite:///./data.db")
    if engine is None or _current_database_url != current_url:
        engine = create_engine(current_url, future=True)
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True, expire_on_commit=False)
        _current_database_url = current_url
    return engine


_initialize_engine()


def init_db() -> None:
    """Create database tables based on models.Base metadata."""
    _initialize_engine()
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    _initialize_engine()
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
