"""Task Service - Business logic for task management"""
from typing import List
from src.domain.task import Task
from src.domain.task_repository import TaskRepository
from .errors import TaskNotFoundError, EmptyDescriptionError


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
