"""Task Repository Interface Contract"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .task import Task


class TaskRepository(ABC):
    """Abstract repository for task storage and retrieval."""

    @abstractmethod
    def add(self, task: Task) -> None:
        """
        Store a new task.

        Args:
            task: Task object to store

        Raises:
            None (implementation-specific errors may be raised)
        """
        pass

    @abstractmethod
    def get(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id: Unique identifier of the task

        Returns:
            Task object if found, None otherwise
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all Task objects (may be empty)
        """
        pass

    @abstractmethod
    def update(self, task: Task) -> None:
        """
        Update an existing task.

        Args:
            task: Task object with updated values

        Raises:
            None (caller should verify task exists before calling)
        """
        pass

    @abstractmethod
    def delete(self, task_id: int) -> None:
        """
        Remove a task from storage.

        Args:
            task_id: Unique identifier of the task to delete

        Raises:
            None (implementation may raise if task not found)
        """
        pass

    @abstractmethod
    def exists(self, task_id: int) -> bool:
        """
        Check if a task exists.

        Args:
            task_id: Unique identifier of the task

        Returns:
            True if task exists, False otherwise
        """
        pass

    @abstractmethod
    def get_next_id(self) -> int:
        """
        Get the next available task ID.

        Returns:
            Next sequential ID for a new task
        """
        pass
