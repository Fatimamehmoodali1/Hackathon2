# Data Model: Phase I Console Todo

**Date**: 2025-12-28
**Purpose**: Define domain entities, state management, and layer interactions

## Domain Entities

### Task

**Purpose**: Represents a single todo item with unique identifier, description, and completion status.

**Attributes**:

| Attribute | Type | Constraints | Default | Description |
|-----------|------|-------------|---------|-------------|
| id | int | Positive integer, unique, never reused | Auto-generated | Unique identifier for the task |
| description | str | Non-empty, supports Unicode | Required | Text describing what needs to be done |
| is_complete | bool | True or False | False | Indicates whether the task is finished |

**Invariants**:
- ID is assigned at creation and never changes (immutable after creation)
- ID sequence is monotonically increasing (1, 2, 3, ...)
- Description cannot be empty string or whitespace-only
- is_complete can be toggled between True and False any number of times
- Task object is mutable (description and is_complete can change, but not id)

**State Transitions**:
```
┌─────────┐
│ Created │ → is_complete = False (default)
└────┬────┘
     │
     ▼
┌─────────┐ ◄────────┐
│ Active  │          │
│ (False) │          │
└────┬────┘          │
     │               │
     │ mark_complete │ mark_incomplete
     │               │
     ▼               │
┌──────────┐         │
│ Complete │ ────────┘
│  (True)  │
└────┬─────┘
     │
     │ delete
     ▼
┌─────────┐
│ Deleted │ (removed from storage)
└─────────┘
```

**Validation Rules**:
- **Description**: `len(description.strip()) > 0`
  - Empty string: ❌ Invalid
  - Whitespace only: ❌ Invalid
  - "Buy groceries": ✅ Valid
  - "   Buy groceries   ": ✅ Valid (will be stripped)
  - Unicode characters: ✅ Valid ("Café ☕")
- **ID**: Positive integer, assigned by system (user cannot set)
  - 0: ❌ Invalid
  - -1: ❌ Invalid
  - 1, 2, 3, ...: ✅ Valid

**Python Implementation**:
```python
from dataclasses import dataclass

@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique identifier (positive integer, auto-assigned)
        description: Task description (non-empty string)
        is_complete: Completion status (default: False)
    """
    id: int
    description: str
    is_complete: bool = False

    def __post_init__(self):
        """Validate task attributes after initialization."""
        if self.id <= 0:
            raise ValueError(f"Task ID must be positive, got: {self.id}")
        if not self.description.strip():
            raise ValueError("Task description cannot be empty")
        # Normalize description (strip whitespace)
        self.description = self.description.strip()
```

## State Management

### Storage Abstraction: TaskRepository

**Purpose**: Abstract interface for task storage, enabling different implementations (in-memory, database, file) without changing business logic.

**Operations**:

| Method | Input | Output | Side Effects | Exceptions |
|--------|-------|--------|--------------|------------|
| add(task) | Task object | None | Stores task in repository | None |
| get(task_id) | int | Optional[Task] | None | None |
| get_all() | None | List[Task] | None | None |
| update(task) | Task object | None | Updates existing task | None |
| delete(task_id) | int | None | Removes task from storage | None |
| exists(task_id) | int | bool | None | None |
| get_next_id() | None | int | Increments internal counter | None |

**Contract Guarantees**:
- `add()`: Task is retrievable via `get()` after adding
- `get()`: Returns None if task doesn't exist (no exception)
- `get_all()`: Returns empty list if no tasks exist (no exception)
- `update()`: Task must exist before updating (caller's responsibility to check)
- `delete()`: Idempotent (deleting non-existent task is safe)
- `exists()`: Always returns bool (never throws exception)
- `get_next_id()`: Returns unique, sequential IDs (never reuses)

### Implementation: InMemoryTaskRepository

**Data Structure**: `dict[int, Task]`
- **Key**: Task ID (int)
- **Value**: Task object
- **Guarantees**:
  - O(1) lookup, insertion, deletion
  - Insertion order preserved (Python 3.7+)
  - Memory efficient for target scale (up to 1000 tasks ≈ 100KB)

**ID Generation Strategy**:
- **Counter**: `_next_id` (private attribute, starts at 1)
- **Increment**: `_next_id += 1` after each task creation
- **Thread-safety**: Not required (single-threaded application)
- **ID Reuse**: Never (counter only increments, even after deletion)

**Memory Management**:
- **Lifetime**: Application runtime only
- **Cleanup**: Automatic (Python garbage collection when app exits)
- **Persistence**: None (data lost on exit, as per specification)

**Python Implementation**:
```python
from typing import Dict, List, Optional

class InMemoryTaskRepository:
    """
    In-memory implementation of TaskRepository.

    Storage: Dictionary mapping task ID to Task object.
    Lifecycle: Data exists only during application runtime.
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task: Task) -> None:
        """Store a task in memory."""
        self._tasks[task.id] = task

    def get(self, task_id: int) -> Optional[Task]:
        """Retrieve task by ID, or None if not found."""
        return self._tasks.get(task_id)

    def get_all(self) -> List[Task]:
        """Retrieve all tasks in insertion order."""
        return list(self._tasks.values())

    def update(self, task: Task) -> None:
        """Update existing task (overwrites)."""
        self._tasks[task.id] = task

    def delete(self, task_id: int) -> None:
        """Remove task (idempotent - no error if not found)."""
        self._tasks.pop(task_id, None)

    def exists(self, task_id: int) -> bool:
        """Check if task exists."""
        return task_id in self._tasks

    def get_next_id(self) -> int:
        """Get next available ID and increment counter."""
        current_id = self._next_id
        self._next_id += 1
        return current_id
```

## Business Logic Layer

### Service: TaskService

**Purpose**: Orchestrate task operations, validate business rules, and translate between repository and domain exceptions.

**Responsibilities**:
1. Validate input (description non-empty, task exists for updates/deletes)
2. Generate IDs for new tasks (via repository.get_next_id())
3. Coordinate repository operations
4. Raise domain exceptions for business rule violations
5. Return domain objects (Task) to callers

**Dependencies**:
- `TaskRepository` (injected via constructor - dependency inversion)

**Methods**:

| Method | Input | Output | Business Logic | Exceptions |
|--------|-------|--------|----------------|------------|
| add_task(desc) | str | Task | Validate desc, get ID, create Task, store | EmptyDescriptionError |
| get_task(id) | int | Task | Retrieve task, raise if not found | TaskNotFoundError |
| get_all_tasks() | None | List[Task] | Return all tasks (may be empty) | None |
| update_task(id, desc) | int, str | Task | Validate desc, check exists, update | TaskNotFoundError, EmptyDescriptionError |
| delete_task(id) | int | None | Check exists, delete | TaskNotFoundError |
| mark_complete(id) | int | Task | Check exists, set is_complete=True, update | TaskNotFoundError |
| mark_incomplete(id) | int | Task | Check exists, set is_complete=False, update | TaskNotFoundError |

**Validation Logic**:

1. **Description Validation**:
   ```python
   def _validate_description(self, description: str) -> str:
       """Validate and normalize description."""
       normalized = description.strip()
       if not normalized:
           raise EmptyDescriptionError()
       return normalized
   ```

2. **Task Existence Validation**:
   ```python
   def _ensure_task_exists(self, task_id: int) -> Task:
       """Retrieve task or raise exception if not found."""
       task = self._repository.get(task_id)
       if task is None:
           raise TaskNotFoundError(task_id)
       return task
   ```

**Python Implementation**:
```python
from typing import List

class TaskService:
    """
    Business logic for task management.

    Responsibilities:
    - Validate business rules
    - Coordinate repository operations
    - Raise domain exceptions
    """

    def __init__(self, repository: TaskRepository):
        self._repository = repository

    def add_task(self, description: str) -> Task:
        """Create and store a new task."""
        validated_desc = self._validate_description(description)
        task_id = self._repository.get_next_id()
        task = Task(id=task_id, description=validated_desc)
        self._repository.add(task)
        return task

    def get_task(self, task_id: int) -> Task:
        """Retrieve task by ID."""
        return self._ensure_task_exists(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks."""
        return self._repository.get_all()

    def update_task(self, task_id: int, description: str) -> Task:
        """Update task description."""
        validated_desc = self._validate_description(description)
        task = self._ensure_task_exists(task_id)
        task.description = validated_desc
        self._repository.update(task)
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task."""
        self._ensure_task_exists(task_id)  # Verify exists before deleting
        self._repository.delete(task_id)

    def mark_complete(self, task_id: int) -> Task:
        """Mark task as complete."""
        task = self._ensure_task_exists(task_id)
        task.is_complete = True
        self._repository.update(task)
        return task

    def mark_incomplete(self, task_id: int) -> Task:
        """Mark task as incomplete."""
        task = self._ensure_task_exists(task_id)
        task.is_complete = False
        self._repository.update(task)
        return task

    def _validate_description(self, description: str) -> str:
        """Validate and normalize description."""
        normalized = description.strip()
        if not normalized:
            raise EmptyDescriptionError()
        return normalized

    def _ensure_task_exists(self, task_id: int) -> Task:
        """Retrieve task or raise exception."""
        task = self._repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task
```

## CLI Presentation Layer

### Components

**1. Menu (`cli/menu.py`)**:
- Display main menu with 7 options
- Capture user choice (1-7)
- Validate choice is numeric and in range
- Route to appropriate command handler
- Loop until user selects Exit (option 7)

**2. Commands (`cli/commands.py`)**:
- One handler function per menu option
- Prompt for required inputs
- Validate input format (CLI layer)
- Call TaskService methods
- Handle domain exceptions
- Display success/error messages

**3. Display (`cli/display.py`)**:
- Format task output (ID, description, status)
- Format messages (error, success, info)
- Consistent styling (borders, spacing)

**Menu Options**:
```
=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete
6. Mark Incomplete
7. Exit

Enter your choice (1-7):
```

**User Flow**:
```
┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Display Menu   │ ◄─────────────┐
└──────┬──────────┘                │
       │                           │
       ▼                           │
┌─────────────────┐                │
│ Get User Choice │                │
└──────┬──────────┘                │
       │                           │
       ├──► 1-6: Execute Command ──┘
       │         (display result,
       │          return to menu)
       │
       └──► 7: Exit
            │
            ▼
         ┌──────┐
         │ End  │
         └──────┘
```

**Error Handling Flow**:
```
User Input → CLI Validation → Service Call → Domain Exception?
                ↓                               ↓
           Invalid Format                   Yes: Catch & Display
                ↓                               ↓
           Display Error                    No: Display Success
                ↓                               ↓
           Return to Menu  ←───────────────────┘
```

## Layer Dependencies

```
┌─────────────────────────────────────────┐
│          CLI Layer (Presentation)        │
│  ┌─────────┐  ┌──────────┐  ┌────────┐ │
│  │  Menu   │  │ Commands │  │Display │ │
│  └────┬────┘  └─────┬────┘  └────────┘ │
└───────┼────────────┼─────────────────────┘
        │            │
        │ depends on │
        │            │
        ▼            ▼
┌─────────────────────────────────────────┐
│      Application Layer (Use Cases)       │
│          ┌──────────────┐                │
│          │ TaskService  │                │
│          └──────┬───────┘                │
└─────────────────┼─────────────────────────┘
                  │ depends on
                  ▼
┌─────────────────────────────────────────┐
│       Domain Layer (Entities)            │
│   ┌────┐  ┌────────────────────┐        │
│   │Task│  │ TaskRepository ABC │        │
│   └────┘  └─────────┬──────────┘        │
└─────────────────────┼─────────────────────┘
                      │ implements
                      ▼
┌─────────────────────────────────────────┐
│    Infrastructure Layer (Storage)        │
│   ┌────────────────────────────┐        │
│   │ InMemoryTaskRepository     │        │
│   └────────────────────────────┘        │
└─────────────────────────────────────────┘
```

**Dependency Rules** (Clean Architecture):
- CLI depends on Application (TaskService)
- Application depends on Domain (Task, TaskRepository interface)
- Infrastructure depends on Domain (implements TaskRepository)
- Domain depends on nothing (pure business logic)

## Data Flow Example: Add Task

```
1. User enters "Buy groceries"
   ↓
2. CLI validates non-empty (format check)
   ↓
3. CLI calls service.add_task("Buy groceries")
   ↓
4. Service validates description (business rule)
   ↓
5. Service calls repository.get_next_id() → 1
   ↓
6. Service creates Task(id=1, description="Buy groceries", is_complete=False)
   ↓
7. Service calls repository.add(task)
   ↓
8. Repository stores task in dict: {1: Task(...)}
   ↓
9. Service returns task to CLI
   ↓
10. CLI displays "✓ Task added successfully (ID: 1)"
    ↓
11. CLI returns to main menu
```

## Performance Characteristics

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| Add Task | O(1) | O(n) | Dictionary insertion |
| Get Task by ID | O(1) | O(1) | Dictionary lookup |
| Get All Tasks | O(n) | O(n) | Iterate dictionary values |
| Update Task | O(1) | O(1) | Dictionary update |
| Delete Task | O(1) | O(1) | Dictionary deletion |
| Mark Complete/Incomplete | O(1) | O(1) | Get + Update |

Where n = number of tasks

**Memory Estimation**:
- Task object: ~200 bytes (id, description, is_complete, Python overhead)
- 100 tasks: ~20 KB
- 1000 tasks: ~200 KB (well within constraints)

## Testing Strategy

**Unit Tests**:
- Task entity validation
- Repository operations (add, get, update, delete)
- Service business logic
- Exception raising and handling

**Integration Tests**:
- End-to-end CLI workflows
- Service + Repository interaction
- Exception propagation through layers

**Acceptance Tests**:
- All 13 acceptance scenarios from spec.md
- All 6 edge cases from spec.md
- Success criteria validation

## Future Phase Evolution

**Phase II (Web Interface)**:
- Keep: Task entity, TaskService, TaskRepository interface
- Replace: CLI with FastAPI endpoints
- Add: DatabaseTaskRepository (replace InMemoryTaskRepository)

**Phase III (Database Persistence)**:
- Keep: Task entity, TaskService, API endpoints
- Replace: InMemoryTaskRepository with SQLModelTaskRepository
- Add: Database migrations, connection pooling

**Phase IV-V**:
- Extend: Task entity (add fields: priority, due_date, category)
- Extend: TaskService (add methods: filter, search, sort)
- Keep: Core architecture intact (layers, dependencies)

This design enables smooth evolution while maintaining core business logic.
