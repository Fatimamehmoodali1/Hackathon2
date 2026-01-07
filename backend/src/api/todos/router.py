"""Todo API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from fastapi.security import HTTPBearer
from typing import List

from core.database import get_db
from core.auth import get_current_user, CurrentUser
from schemas import TodoCreate, TodoUpdate, TodoToggle, TodoResponse, TodoListResponse
from services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["Todos"])
security = HTTPBearer()


@router.get("", response_model=TodoListResponse)
def get_todos(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TodoListResponse:
    """Get all todos for the authenticated user."""
    todos = TodoService.get_user_todos(db, current_user.id)

    return TodoListResponse(
        todos=[TodoResponse.model_validate(todo) for todo in todos],
        count=len(todos),
    )


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_data: TodoCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TodoResponse:
    """Create a new todo."""
    todo = TodoService.create_todo(db, current_user.id, todo_data)
    return TodoResponse.model_validate(todo)


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TodoResponse:
    """Get a specific todo by ID."""
    todo = TodoService.get_todo_by_id(db, todo_id, current_user.id)
    return TodoResponse.model_validate(todo)


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TodoResponse:
    """Update a todo."""
    todo = TodoService.update_todo(db, todo_id, current_user.id, todo_data)
    return TodoResponse.model_validate(todo)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Delete a todo."""
    TodoService.delete_todo(db, todo_id, current_user.id)


@router.patch("/{todo_id}/toggle", response_model=TodoResponse)
def toggle_todo(
    todo_id: int,
    toggle_data: TodoToggle,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TodoResponse:
    """Toggle todo completion status."""
    todo = TodoService.toggle_todo(
        db, todo_id, current_user.id, toggle_data.is_complete
    )
    return TodoResponse.model_validate(todo)
