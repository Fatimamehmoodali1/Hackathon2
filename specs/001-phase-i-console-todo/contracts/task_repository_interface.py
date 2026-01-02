"""
Task Repository Interface Contract

This defines the abstract interface that all task storage implementations must follow.
Phase I uses InMemoryTaskRepository; future phases may add DatabaseTaskRepository.

Version: 1.0.0
Phase: I
"""

from abc import ABC, abstractmethod
from typing import List, Optional


class TaskRepository(ABC):
    """
    Abstract repository for task storage and retrieval.

    This interface defines the contract that all task storage implementations
    must satisfy. It abstracts away the storage mechanism (in-memory, database,
    file, etc.) allowing the business logic to remain independent of storage details.

    Implementations must guarantee:
    - Thread-safety (if applicable to the implementation)
    - Idempotent operations where noted
    - Consistent ID generation (sequential, never reused)
    """

    @abstractmethod
    def add(self, task: 'Task') -> None:
        """
        Store a new task.

        After successful addition, the task must be retrievable via get(task.id).

        Args:
            task: Task object to store (with ID already assigned)

        Returns:
            None

        Raises:
            None (implementations may raise storage-specific errors)

        Guarantees:
            - Task is stored and retrievable immediately
            - Existing task with same ID is overwritten (upsert behavior)
        """
        pass

    @abstractmethod
    def get(self, task_id: int) -> Optional['Task']:
        """
        Retrieve a task by its ID.

        Args:
            task_id: Unique identifier of the task

        Returns:
            Task object if found, None if not found

        Raises:
            None (returns None instead of raising exception)

        Guarantees:
            - Returns same task object as was added
            - Never raises exception for non-existent task
        """
        pass

    @abstractmethod
    def get_all(self) -> List['Task']:
        """
        Retrieve all tasks.

        Returns:
            List of all Task objects (may be empty if no tasks exist)
            Order: Insertion order (first added → first in list)

        Raises:
            None

        Guarantees:
            - Returns empty list if no tasks exist (never None)
            - Returns all tasks that have been added and not deleted
            - Order is consistent with insertion order
        """
        pass

    @abstractmethod
    def update(self, task: 'Task') -> None:
        """
        Update an existing task.

        This overwrites the existing task with the same ID. Caller is responsible
        for ensuring the task exists before calling (use exists() or get()).

        Args:
            task: Task object with updated values

        Returns:
            None

        Raises:
            None (caller should verify task exists before calling)

        Guarantees:
            - Task is updated immediately
            - Subsequent get() returns updated task
        """
        pass

    @abstractmethod
    def delete(self, task_id: int) -> None:
        """
        Remove a task from storage.

        Idempotent operation: deleting a non-existent task is safe (no error).

        Args:
            task_id: Unique identifier of the task to delete

        Returns:
            None

        Raises:
            None (idempotent - no error if task doesn't exist)

        Guarantees:
            - Task is no longer retrievable via get() after deletion
            - Subsequent delete() of same ID is safe (no error)
            - ID is never reused, even after deletion
        """
        pass

    @abstractmethod
    def exists(self, task_id: int) -> bool:
        """
        Check if a task exists.

        Args:
            task_id: Unique identifier of the task

        Returns:
            True if task with given ID exists, False otherwise

        Raises:
            None

        Guarantees:
            - Always returns bool (never None or exception)
            - Consistent with get() result (exists=True ⟺ get()!=None)
        """
        pass

    @abstractmethod
    def get_next_id(self) -> int:
        """
        Get the next available task ID.

        IDs must be:
        - Sequential (1, 2, 3, ...)
        - Unique (never reused, even after deletion)
        - Monotonically increasing (never decreasing)

        Returns:
            Next sequential ID for a new task (starting from 1)

        Raises:
            None

        Guarantees:
            - Returns unique ID not used by any existing or deleted task
            - Subsequent calls return strictly increasing IDs
            - First call returns 1, then 2, 3, etc.
        """
        pass


# Type hint for Task (avoid circular import)
# In actual implementation, import from domain.task
class Task:
    """
    Placeholder for Task type hint.
    Actual implementation in src/domain/task.py
    """
    id: int
    description: str
    is_complete: bool
