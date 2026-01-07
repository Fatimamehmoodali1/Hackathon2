"""Todo Pydantic schemas for API request/response validation."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    """Schema for creating a todo."""

    title: str = Field(..., min_length=1, max_length=200)


class TodoUpdate(BaseModel):
    """Schema for updating a todo."""

    title: str = Field(..., min_length=1, max_length=200)


class TodoToggle(BaseModel):
    """Schema for toggling todo completion."""

    is_complete: bool


class TodoResponse(BaseModel):
    """Schema for todo response."""

    id: int
    user_id: int
    title: str
    is_complete: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoListResponse(BaseModel):
    """Schema for list of todos response."""

    todos: List[TodoResponse]
    count: int
