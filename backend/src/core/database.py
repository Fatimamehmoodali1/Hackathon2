"""Database connection and session management for SQLModel."""
from contextlib import contextmanager
from typing import Generator, Optional
from sqlmodel import SQLModel, create_engine, Session, Engine
from .config import settings

# Lazy engine initialization for Vercel serverless
_engine: Optional[Engine] = None


def get_engine() -> Engine:
    """Get or create database engine."""
    global _engine
    if _engine is None:
        # Create engine - PostgreSQL/SQLite support
        connect_args = {}
        if "sqlite" in settings.database_url:
            connect_args = {"check_same_thread": False}
        elif "postgresql" in settings.database_url:
            # Neon PostgreSQL requires SSL
            connect_args = {"sslmode": "require"}

        _engine = create_engine(
            settings.database_url,
            echo=False,
            connect_args=connect_args,
            pool_pre_ping=True,  # Verify connections before using
        )
    return _engine


def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a database session."""
    engine = get_engine()
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
    engine = get_engine()
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise


def init_db() -> None:
    """Initialize database tables."""
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


def close_db() -> None:
    """Close database connections."""
    engine = get_engine()
    engine.dispose()
