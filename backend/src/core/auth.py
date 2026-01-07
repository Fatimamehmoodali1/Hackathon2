"""Authentication utilities using Better Auth."""
from datetime import datetime, timedelta
from typing import Optional
from dataclasses import dataclass
import bcrypt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select

from .database import get_db
from models import User

security = HTTPBearer()


@dataclass
class CurrentUser:
    """Represents the currently authenticated user."""

    id: int
    email: str


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> CurrentUser:
    """Dependency to get the current authenticated user from the session token.

    For Phase II, we use a simple JWT-like token approach since Better Auth
    Python SDK has specific integration patterns. The token contains the user ID.
    """
    token = credentials.credentials

    try:
        user_id = int(token)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    user = db.exec(select(User).where(User.id == user_id)).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return CurrentUser(id=user.id, email=user.email)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a hash."""
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8"),
    )


def create_session_token(user_id: int) -> str:
    """Create a simple session token (for Phase II - replace with proper JWT in production)."""
    return str(user_id)
