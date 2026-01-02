"""Task entity - represents a single todo item"""
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
