"""
Task Service Interface Contract

This defines the public API for task management business logic.
All CLI commands interact with tasks through this service interface.

Version: 1.0.0
Phase: I
"""

from abc import ABC, abstractmethod
from typing import List


class TaskService(ABC):
    """
    Abstract service for task management operations.

    This interface defines the contract for task management business logic.
    It sits between the presentation layer (CLI) and the domain/infrastructure
    layers, orchestrating operations and enforcing business rules.

    Responsibilities:
    - Validate business rules (non-empty description, task existence)
    - Coordinate repository operations
    - Raise domain exceptions for violations
    - Return domain objects (Task) to callers

    Error Handling:
    - Raises domain exceptions (not generic exceptions)
    - Never returns None for operations that should return Task
    - Validation happens before repository operations
    """

    @abstractmethod
    def add_task(self, description: str) -> 'Task':
        """
        Create and store a new task.

        Business Rules:
        - Description cannot be empty or whitespace-only
        - Description is normalized (leading/trailing whitespace stripped)
        - ID is auto-generated and sequential

        Args:
            description: Task description text (will be normalized)

        Returns:
            Created Task object with assigned ID and is_complete=False

        Raises:
            EmptyDescriptionError: If description is empty or whitespace-only

        Example:
            >>> task = service.add_task("Buy groceries")
            >>> task.id  # 1 (auto-assigned)
            >>> task.description  # "Buy groceries" (normalized)
            >>> task.is_complete  # False (default)
        """
        pass

    @abstractmethod
    def get_task(self, task_id: int) -> 'Task':
        """
        Retrieve a task by ID.

        Business Rules:
        - Task ID must refer to an existing task
        - Returns task object (never None)

        Args:
            task_id: Unique identifier of the task

        Returns:
            Task object with given ID

        Raises:
            TaskNotFoundError: If task with given ID doesn't exist

        Example:
            >>> task = service.get_task(1)
            >>> task.description  # "Buy groceries"

            >>> service.get_task(999)  # Raises TaskNotFoundError
        """
        pass

    @abstractmethod
    def get_all_tasks(self) -> List['Task']:
        """
        Retrieve all tasks.

        Business Rules:
        - Returns all tasks in insertion order
        - Returns empty list if no tasks exist (never None)

        Returns:
            List of all Task objects (may be empty)

        Raises:
            None

        Example:
            >>> tasks = service.get_all_tasks()
            >>> len(tasks)  # 2
            >>> tasks[0].description  # "Buy groceries"
            >>> tasks[1].description  # "Call dentist"
        """
        pass

    @abstractmethod
    def update_task(self, task_id: int, description: str) -> 'Task':
        """
        Update a task's description.

        Business Rules:
        - Task ID must refer to an existing task
        - Description cannot be empty or whitespace-only
        - Description is normalized (leading/trailing whitespace stripped)
        - Completion status is unchanged

        Args:
            task_id: Unique identifier of the task to update
            description: New description text (will be normalized)

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task with given ID doesn't exist
            EmptyDescriptionError: If description is empty or whitespace-only

        Example:
            >>> task = service.update_task(1, "Buy groceries and milk")
            >>> task.description  # "Buy groceries and milk"
            >>> task.is_complete  # Unchanged
        """
        pass

    @abstractmethod
    def delete_task(self, task_id: int) -> None:
        """
        Delete a task.

        Business Rules:
        - Task ID must refer to an existing task
        - Deleted task ID is never reused

        Args:
            task_id: Unique identifier of the task to delete

        Returns:
            None

        Raises:
            TaskNotFoundError: If task with given ID doesn't exist

        Example:
            >>> service.delete_task(1)  # Task removed
            >>> service.get_task(1)  # Raises TaskNotFoundError
        """
        pass

    @abstractmethod
    def mark_complete(self, task_id: int) -> 'Task':
        """
        Mark a task as complete.

        Business Rules:
        - Task ID must refer to an existing task
        - Sets is_complete=True
        - Idempotent (marking complete task as complete is safe)
        - Description is unchanged

        Args:
            task_id: Unique identifier of the task

        Returns:
            Updated Task object with is_complete=True

        Raises:
            TaskNotFoundError: If task with given ID doesn't exist

        Example:
            >>> task = service.mark_complete(1)
            >>> task.is_complete  # True
            >>> task.description  # Unchanged
        """
        pass

    @abstractmethod
    def mark_incomplete(self, task_id: int) -> 'Task':
        """
        Mark a task as incomplete.

        Business Rules:
        - Task ID must refer to an existing task
        - Sets is_complete=False
        - Idempotent (marking incomplete task as incomplete is safe)
        - Description is unchanged

        Args:
            task_id: Unique identifier of the task

        Returns:
            Updated Task object with is_complete=False

        Raises:
            TaskNotFoundError: If task with given ID doesn't exist

        Example:
            >>> task = service.mark_incomplete(1)
            >>> task.is_complete  # False
            >>> task.description  # Unchanged
        """
        pass


# Domain Exception Types (defined in src/application/errors.py)
class TodoError(Exception):
    """Base exception for all todo application errors."""
    pass


class TaskNotFoundError(TodoError):
    """Raised when a task with given ID doesn't exist."""
    pass


class EmptyDescriptionError(TodoError):
    """Raised when task description is empty."""
    pass


# Type hint for Task (avoid circular import)
class Task:
    """
    Placeholder for Task type hint.
    Actual implementation in src/domain/task.py
    """
    id: int
    description: str
    is_complete: bool
