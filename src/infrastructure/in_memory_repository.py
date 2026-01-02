"""In-memory implementation of TaskRepository"""
from typing import Dict, List, Optional
from src.domain.task import Task
from src.domain.task_repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):
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
