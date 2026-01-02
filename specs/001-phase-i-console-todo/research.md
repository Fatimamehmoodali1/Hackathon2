# Research Findings: Phase I Console Todo

**Date**: 2025-12-28
**Purpose**: Resolve technical unknowns and establish implementation patterns for Phase I

## 1. ID Generation Strategy

**Decision**: Simple counter with monotonically increasing integers

**Rationale**:
- Meets all requirements (sequential, never reused, starts at 1)
- Simplest possible implementation (single integer variable)
- No external dependencies needed
- Performance: O(1) for ID generation
- Easy to understand and maintain
- No collision risks in single-threaded environment

**Alternatives Considered**:
- **UUID**: Rejected (overkill for single-user app, not sequential, harder to read)
- **Timestamp-based**: Rejected (not guaranteed sequential, potential collisions, timezone issues)
- **Hash-based**: Rejected (not sequential, unnecessary complexity)

**Implementation Approach**:
```python
class InMemoryTaskRepository:
    def __init__(self):
        self._next_id = 1
        self._tasks = {}

    def get_next_id(self):
        current_id = self._next_id
        self._next_id += 1
        return current_id
```

## 2. In-Memory Storage Pattern

**Decision**: Dictionary with integer keys (task ID → Task object)

**Rationale**:
- O(1) lookup by ID for all operations (get, update, delete)
- Preserves insertion order (Python 3.7+ dict guarantee)
- Supports efficient deletion without shifting IDs
- Simple iteration for "View All" operation
- Native Python data structure (no external dependencies)
- Memory efficient for target scale (up to 1000 tasks)

**Alternatives Considered**:
- **List with index = ID**: Rejected (O(n) lookup after deletions, ID gaps complicate indexing, memory waste with sparse IDs)
- **OrderedDict**: Rejected (dict preserves order since Python 3.7, OrderedDict adds unnecessary overhead)
- **Custom linked structure**: Rejected (unnecessary complexity, no performance benefit)
- **Dataclass with list**: Rejected (same issues as plain list)

**Implementation Approach**:
```python
class InMemoryTaskRepository:
    def __init__(self):
        self._tasks: dict[int, Task] = {}

    def add(self, task: Task) -> None:
        self._tasks[task.id] = task

    def get(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def get_all(self) -> List[Task]:
        return list(self._tasks.values())

    def delete(self, task_id: int) -> None:
        self._tasks.pop(task_id, None)
```

**Performance Characteristics**:
- Add: O(1)
- Get by ID: O(1)
- Get all: O(n) where n = number of tasks
- Update: O(1)
- Delete: O(1)
- Memory: O(n) where n = number of tasks

## 3. CLI Input Validation

**Decision**: Separate validation functions with early returns

**Rationale**:
- Clear separation of concerns (validation vs business logic)
- Reusable validation functions across commands
- Easy to test in isolation (unit tests for validators)
- Explicit error messages for each validation rule
- Fails fast (return error before processing)
- Simple to extend with new validation rules

**Alternatives Considered**:
- **Inline validation**: Rejected (clutters business logic, hard to test, duplicated code)
- **Decorator-based**: Rejected (over-engineered for Phase I scope, harder to debug)
- **Schema validation library (Pydantic)**: Rejected (external dependency, overkill for simple validation)
- **Try-except blocks**: Rejected (less explicit, harder to provide specific error messages)

**Implementation Approach**:
```python
# In cli/validation.py
def validate_task_id(user_input: str) -> tuple[bool, int | str]:
    """
    Validate task ID input.

    Returns:
        (True, task_id) if valid, (False, error_message) if invalid
    """
    try:
        task_id = int(user_input)
        if task_id <= 0:
            return False, "Task ID must be a positive number"
        return True, task_id
    except ValueError:
        return False, "Invalid task ID format. Please enter a number."

def validate_description(description: str) -> tuple[bool, str]:
    """
    Validate task description input.

    Returns:
        (True, description) if valid, (False, error_message) if invalid
    """
    stripped = description.strip()
    if not stripped:
        return False, "Task description cannot be empty"
    return True, stripped
```

**Usage in Commands**:
```python
# In cli/commands.py
def handle_add_task(service: TaskService):
    description = input("Enter task description: ")
    is_valid, result = validate_description(description)

    if not is_valid:
        print(f"Error: {result}")
        return

    try:
        task = service.add_task(result)
        print(f"✓ Task added successfully (ID: {task.id})")
    except Exception as e:
        print(f"Error: {e}")
```

## 4. Error Handling Strategy

**Decision**: Custom domain exceptions with message templates

**Rationale**:
- Type-safe error handling (catch specific exceptions)
- Consistent error messages (templates in one place)
- Clean separation (domain exceptions vs infrastructure errors)
- Easy to extend for future phases
- Pythonic approach (exceptions for exceptional conditions)
- Clear error propagation through layers

**Exception Hierarchy**:
```
TodoError (base exception)
├── TaskNotFoundError(task_id)
├── InvalidTaskIdError(input_value)
└── EmptyDescriptionError()
```

**Alternatives Considered**:
- **Generic exceptions**: Rejected (loses type information, hard to handle specific cases)
- **Error codes/tuples**: Rejected (less Pythonic, harder to handle, no stack traces)
- **Result/Option types**: Rejected (not idiomatic Python, adds complexity)
- **Logging only**: Rejected (doesn't allow recovery, hard to test)

**Implementation Approach**:
```python
# In application/errors.py
class TodoError(Exception):
    """Base exception for all todo application errors."""
    pass

class TaskNotFoundError(TodoError):
    """Raised when a task with given ID doesn't exist."""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task not found with ID: {task_id}")

class InvalidTaskIdError(TodoError):
    """Raised when task ID is invalid."""
    def __init__(self, input_value: str):
        self.input_value = input_value
        super().__init__(f"Invalid task ID format: {input_value}")

class EmptyDescriptionError(TodoError):
    """Raised when task description is empty."""
    def __init__(self):
        super().__init__("Task description cannot be empty")
```

**Error Handling Flow**:
1. CLI validates input format (numeric IDs, non-empty strings)
2. Service validates business rules (description not empty)
3. Service raises domain exceptions for violations
4. CLI catches exceptions and displays user-friendly messages
5. Application never crashes (graceful degradation)

## 5. Testing Approach

**Decision**: pytest with fixture-based setup, AAA pattern

**Rationale**:
- Industry standard for Python testing
- Excellent fixture support for test isolation
- Clear test structure (Arrange-Act-Assert)
- Coverage plugin available
- Parametrized tests for multiple scenarios
- Easy to run subset of tests
- Good IDE integration

**Test Organization**:
```
tests/
├── unit/
│   ├── test_task.py                   # Task entity tests
│   ├── test_task_service.py           # Service layer tests
│   └── test_in_memory_repository.py   # Repository tests
├── integration/
│   ├── test_cli_workflows.py          # End-to-end CLI tests
│   └── test_acceptance_scenarios.py   # Spec acceptance criteria
└── conftest.py                        # Shared fixtures
```

**Alternatives Considered**:
- **unittest**: Rejected (more verbose, class-based, setUp/tearDown boilerplate)
- **doctest**: Rejected (insufficient for acceptance scenarios, clutters docstrings)
- **nose/nose2**: Rejected (pytest is more actively maintained and feature-rich)
- **hypothesis**: Rejected (property-based testing overkill for Phase I scope)

**Implementation Approach**:

**conftest.py** (Shared Fixtures):
```python
import pytest
from src.domain.task import Task
from src.infrastructure.in_memory_repository import InMemoryTaskRepository
from src.application.task_service import TaskService

@pytest.fixture
def repository():
    """Provide a fresh in-memory repository for each test."""
    return InMemoryTaskRepository()

@pytest.fixture
def service(repository):
    """Provide a task service with fresh repository."""
    return TaskService(repository)

@pytest.fixture
def sample_tasks():
    """Provide sample tasks for testing."""
    return [
        Task(id=1, description="Buy groceries", is_complete=False),
        Task(id=2, description="Call dentist", is_complete=True),
        Task(id=3, description="Write report", is_complete=False),
    ]
```

**Test Structure (AAA Pattern)**:
```python
# tests/unit/test_task_service.py
def test_add_task_with_valid_description(service):
    # Arrange
    description = "Buy groceries"

    # Act
    task = service.add_task(description)

    # Assert
    assert task.id == 1
    assert task.description == "Buy groceries"
    assert task.is_complete is False

def test_add_task_with_empty_description_raises_error(service):
    # Arrange
    description = "   "  # Whitespace only

    # Act & Assert
    with pytest.raises(EmptyDescriptionError):
        service.add_task(description)
```

**Coverage Goals**:
- Domain layer: 100% (simple entities, full coverage is achievable)
- Application layer: >95% (core business logic, critical for correctness)
- Infrastructure layer: >90% (repository operations, straightforward)
- CLI layer: >80% (harder to test, focus on integration tests)
- Overall: >90% coverage

**Test Execution**:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_task.py

# Run tests matching pattern
pytest -k "add_task"

# Verbose output
pytest -v
```

## 6. Python Project Structure Best Practices

**Decision**: Standard src-layout with package-based organization

**Rationale**:
- Prevents accidental imports of test code
- Clear separation between source and tests
- Standard Python packaging convention
- Easy to distribute as package later
- Supports proper import paths

**Structure**:
```
phase1/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── cli/
├── tests/
│   ├── unit/
│   └── integration/
├── specs/
├── requirements.txt
└── requirements-dev.txt
```

## 7. Development Dependencies

**Decision**: Minimal dependencies with clear separation (production vs dev)

**Production Dependencies** (requirements.txt):
```
# None - standard library only
```

**Development Dependencies** (requirements-dev.txt):
```
pytest==7.4.3
pytest-cov==4.1.0
black==23.12.1
pylint==3.0.3
mypy==1.7.1
```

**Rationale**:
- No production dependencies (Phase I constraint)
- pytest for testing (industry standard)
- pytest-cov for coverage reporting
- black for code formatting (consistent style)
- pylint for linting (catch errors)
- mypy for type checking (static analysis)

## 8. Type Hints Strategy

**Decision**: Full type hints for all functions and classes

**Rationale**:
- Catch errors at development time (mypy)
- Better IDE support (autocomplete, refactoring)
- Self-documenting code
- Easier to maintain and refactor
- Constitutional quality standards

**Implementation**:
```python
from typing import List, Optional

class Task:
    def __init__(self, id: int, description: str, is_complete: bool = False) -> None:
        self.id = id
        self.description = description
        self.is_complete = is_complete

class TaskService:
    def add_task(self, description: str) -> Task:
        ...

    def get_task(self, task_id: int) -> Task:
        ...

    def get_all_tasks(self) -> List[Task]:
        ...
```

## Summary of Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| ID Generation | Simple counter | Simplest, meets all requirements |
| Storage | dict[int, Task] | O(1) operations, preserves order |
| Validation | Separate functions | Reusable, testable, explicit errors |
| Errors | Domain exceptions | Type-safe, Pythonic, extensible |
| Testing | pytest + fixtures | Industry standard, excellent support |
| Structure | src-layout | Best practice, supports packaging |
| Dependencies | Minimal (dev only) | Meets Phase I constraints |
| Type Hints | Full coverage | Quality, maintainability, tooling |

All decisions support Phase I requirements while enabling smooth evolution to future phases.
