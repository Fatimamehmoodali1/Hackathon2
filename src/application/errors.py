"""Domain exceptions for todo application"""


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
