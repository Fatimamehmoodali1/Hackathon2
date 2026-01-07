# Data Model: Phase II Full-Stack Todo Application

**Date**: 2026-01-04
**Feature**: Phase II - Full-Stack Todo Application
**Status**: Approved

---

## Entity Overview

| Entity | Description | Relationships |
|--------|-------------|---------------|
| User | Authenticated user account | 1-to-Many with Todo |
| Todo | Task item belonging to a user | Many-to-1 with User |

---

## User Entity

### Definition

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List

class User(SQLModel, table=True):
    """Authenticated user account in the system."""

    id: int | None = Field(default=None, primary_key=True)
    """Unique identifier for the user."""

    email: str = Field(unique=True, index=True, max_length=255)
    """User's email address (unique across all users)."""

    password_hash: str = Field(max_length=255)
    """BCRYPT hashed password (never store plain text)."""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    """Timestamp when the account was created (UTC)."""

    # Relationships
    todos: List["Todo"] = Relationship(back_populates="user")
    """All todos belonging to this user."""
```

### Constraints

| Field | Constraint | Reason |
|-------|------------|--------|
| id | Primary key, auto-increment | Unique identification |
| email | UNIQUE, NOT NULL, max 255 chars | Prevent duplicates, ensure validity |
| password_hash | NOT NULL, max 255 chars | Required for authentication |
| created_at | NOT NULL, default NOW | Audit trail |

### Indexes

- `idx_user_email`: ON `email` for fast lookups during signin

---

## Todo Entity

### Definition

```python
class Todo(SQLModel, table=True):
    """Task item belonging to a user."""

    id: int | None = Field(default=None, primary_key=True)
    """Unique identifier for the todo."""

    user_id: int = Field(foreign_key="user.id", on_delete="CASCADE")
    """Reference to the owning user."""

    title: str = Field(max_length=200)
    """The todo's task description."""

    is_complete: bool = Field(default=False)
    """Whether the todo has been completed."""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    """Timestamp when the todo was created (UTC)."""

    updated_at: datetime = Field(default_factory=datetime.utcnow)
    """Timestamp when the todo was last modified (UTC)."""

    # Relationships
    user: User = Relationship(back_populates="todos")
    """The user who owns this todo."""
```

### Constraints

| Field | Constraint | Reason |
|-------|------------|--------|
| id | Primary key, auto-increment | Unique identification |
| user_id | NOT NULL, FK to user.id | Ownership tracking |
| title | NOT NULL, max 200 chars | Required field, prevent abuse |
| is_complete | NOT NULL, default FALSE | Track completion state |
| created_at | NOT NULL, default NOW | Audit trail |
| updated_at | NOT NULL, default NOW | Modification tracking |

### Indexes

- `idx_todo_user_id`: ON `user_id` for filtering user's todos
- Composite index for common queries if needed

---

## Relationship: User → Todo

**Type**: One-to-Many (Unidirectional from User)

**Foreign Key**: `todos.user_id` → `users.id`

**Referential Integrity Rules**:
- ON DELETE CASCADE: Deleting a user removes all their todos
- ON UPDATE CASCADE: User id changes propagate to todos

**ER Diagram**:

```
┌─────────────┐       1       ┌─────────────┐
│    User     │───────────────│    Todo     │
│─────────────│               │─────────────│
│ id          │               │ id          │
│ email       │               │ user_id ────┘
│ password_h  │               │ title       │
│ created_at  │               │ is_complete │
└─────────────┘               │ created_at  │
                              │ updated_at  │
                              └─────────────┘
```

---

## Validation Rules

### User Validation

| Rule | Validation Type | Error Code |
|------|-----------------|------------|
| Email format valid | Pydantic EmailStr | 400 |
| Email unique | Database UNIQUE constraint | 400 |
| Password minimum 8 chars | Pydantic min_length | 400 |

### Todo Validation

| Rule | Validation Type | Error Code |
|------|-----------------|------------|
| Title not empty | Pydantic min_length=1 | 400 |
| Title max 200 chars | Pydantic max_length=200 | 400 |
| User exists | Database FK constraint | 400 |

---

## State Transitions

### Todo Lifecycle

```
┌──────────────┐
│   Created    │
└──────┬───────┘
       │ (user creates todo)
       ▼
┌──────────────┐
│   Pending    │ ←──────────────┐
│ (incomplete) │                │
└──────┬───────┘                │ (user toggles)
       │                        │
       │ (user toggles)         │
       ▼                        │
┌──────────────┐                │
│   Complete   │                │
└──────┬───────┘                │
       │ (user toggles)         │
       ▼                        │
┌──────────────┐                │
│   Pending    │ ───────────────┘
│ (incomplete) │
└──────┬───────┘
       │ (user deletes)
       ▼
┌──────────────┐
│   Deleted    │
└──────────────┘
```

**Valid Transitions**:
- Pending → Complete (toggle)
- Complete → Pending (toggle)
- Any state → Deleted (delete)

---

## Database Schema (PostgreSQL)

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- Todos table
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    is_complete BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_todos_user_id ON todos(user_id);
```

---

## API Schemas (Pydantic)

### User Schemas

```python
from pydantic import EmailStr, BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    """Request schema for user registration."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserResponse(BaseModel):
    """Response schema for user data (without password)."""
    id: int
    email: str
    created_at: datetime

class UserLogin(BaseModel):
    """Request schema for user signin."""
    email: EmailStr
    password: str
```

### Todo Schemas

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TodoCreate(BaseModel):
    """Request schema for creating a todo."""
    title: str = Field(min_length=1, max_length=200)

class TodoUpdate(BaseModel):
    """Request schema for updating a todo."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)

class TodoResponse(BaseModel):
    """Response schema for todo data."""
    id: int
    user_id: int
    title: str
    is_complete: bool
    created_at: datetime
    updated_at: datetime

class TodoListResponse(BaseModel):
    """Response schema for list of todos."""
    todos: list[TodoResponse]
    count: int
```

### Error Schemas

```python
class ErrorResponse(BaseModel):
    """Standard error response."""
    error: dict
```

---

## Migration Strategy

### Version 1 (Initial)

1. Create `users` table with all User columns
2. Create `todos` table with all Todo columns
3. Create foreign key constraint with CASCADE
4. Create indexes for performance

### Future Versions (if needed)

- Alembic handles incremental migrations
- Down migrations available for rollback
- Zero-downtime migration support via caution

---

## Notes

- All timestamps stored in UTC
- All string lengths are max limits (actual data may be shorter)
- Password never stored in plain text
- No soft delete implemented for Phase II
