"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from fastapi.security import HTTPBearer

from core.database import get_db
from schemas import UserCreate, UserResponse
from services.auth_service import AuthService
from core.auth import create_session_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db),
) -> dict:
    """Register a new user account."""
    user = AuthService.create_user(db, user_data)

    return {
        "message": "Account created successfully",
        "user": {
            "id": user.id,
            "email": user.email,
        },
    }


@router.post("/signin")
def signin(
    credentials: UserCreate,
    db: Session = Depends(get_db),
) -> dict:
    """Authenticate user and return session token."""
    user = AuthService.authenticate_user(db, credentials.email, credentials.password)

    token = create_session_token(user.id)

    return {
        "message": "Sign in successful",
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
        },
    }


@router.post("/signout")
def signout() -> dict:
    """Sign out the current user."""
    return {"message": "Sign out successful"}


@router.get("/me")
def get_me(
    credentials: HTTPBearer = Depends(HTTPBearer()),
    db: Session = Depends(get_db),
) -> dict:
    """Get current authenticated user info."""
    from core.auth import get_current_user
    from schemas import UserResponse

    current_user = get_current_user(credentials, db)

    user = AuthService.get_user_by_id(db, current_user.id)

    return {
        "user": UserResponse.model_validate(user),
    }
