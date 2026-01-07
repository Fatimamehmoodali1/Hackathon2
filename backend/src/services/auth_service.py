"""Authentication service for user management."""
from sqlmodel import Session, select
from fastapi import HTTPException, status

from models import User
from schemas import UserCreate
from core.auth import hash_password, verify_password, create_session_token


class AuthService:
    """Service for authentication-related operations."""

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user account."""
        # Check if email already exists
        existing_user = db.exec(select(User).where(User.email == user_data.email)).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists",
            )

        # Create new user
        hashed_password = hash_password(user_data.password)
        user = User(
            email=user_data.email,
            password_hash=hashed_password,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """Authenticate a user with email and password."""
        user = db.exec(select(User).where(User.email == email)).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        """Get a user by ID."""
        return db.exec(select(User).where(User.id == user_id)).first()
