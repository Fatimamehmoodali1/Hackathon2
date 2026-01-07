"""Database connection and session management for SQLModel."""
from contextlib import contextmanager
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
from .config import settings

# Create engine - SQLite for development
engine = create_engine(
    settings.database_url,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
)


def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a database session."""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """Context manager for database sessions (for use outside of FastAPI dependencies)."""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise


def init_db() -> None:
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)


def close_db() -> None:
    """Close database connections."""
    engine.dispose()
