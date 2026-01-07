"""Todo service for CRUD operations."""
from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException, status

from models import Todo
from schemas import TodoCreate, TodoUpdate


class TodoService:
    """Service for todo-related operations."""

    @staticmethod
    def get_user_todos(db: Session, user_id: int) -> List[Todo]:
        """Get all todos for a user."""
        todos = db.exec(
            select(Todo)
            .where(Todo.user_id == user_id)
            .order_by(Todo.created_at.desc())
        ).all()
        return list(todos)

    @staticmethod
    def get_todo_by_id(db: Session, todo_id: int, user_id: int) -> Todo:
        """Get a specific todo by ID, verifying ownership."""
        todo = db.exec(select(Todo).where(Todo.id == todo_id)).first()

        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found",
            )

        if todo.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this todo",
            )

        return todo

    @staticmethod
    def create_todo(db: Session, user_id: int, todo_data: TodoCreate) -> Todo:
        """Create a new todo for a user."""
        todo = Todo(
            user_id=user_id,
            title=todo_data.title,
        )
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    @staticmethod
    def update_todo(
        db: Session, todo_id: int, user_id: int, todo_data: TodoUpdate
    ) -> Todo:
        """Update a todo, verifying ownership."""
        todo = TodoService.get_todo_by_id(db, todo_id, user_id)

        todo.title = todo_data.title
        todo.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(todo)
        return todo

    @staticmethod
    def toggle_todo(
        db: Session, todo_id: int, user_id: int, is_complete: bool
    ) -> Todo:
        """Toggle todo completion status, verifying ownership."""
        todo = TodoService.get_todo_by_id(db, todo_id, user_id)

        todo.is_complete = is_complete
        todo.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(todo)
        return todo

    @staticmethod
    def delete_todo(db: Session, todo_id: int, user_id: int) -> None:
        """Delete a todo, verifying ownership."""
        todo = TodoService.get_todo_by_id(db, todo_id, user_id)

        db.delete(todo)
        db.commit()
