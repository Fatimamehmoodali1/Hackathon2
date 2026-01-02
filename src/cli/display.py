"""Display utilities for CLI interface"""
from typing import List
from src.domain.task import Task


def display_menu() -> None:
    """Display the main menu options."""
    print("\n=== Todo Application ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete")
    print("6. Mark Incomplete")
    print("7. Exit")


def display_tasks(tasks: List[Task]) -> None:
    """
    Display a formatted list of tasks.

    Args:
        tasks: List of Task objects to display
    """
    if not tasks:
        print("\nNo tasks found")
        return

    print("\n=== All Tasks ===")
    for task in tasks:
        status = "Complete" if task.is_complete else "Incomplete"
        print(f"ID: {task.id} | {task.description} | Status: {status}")


def display_message(msg_type: str, text: str) -> None:
    """
    Display a formatted message.

    Args:
        msg_type: Type of message (success, error, info)
        text: Message text to display
    """
    if msg_type == "success":
        print(f"\n✓ {text}")
    elif msg_type == "error":
        print(f"\n✗ Error: {text}")
    elif msg_type == "info":
        print(f"\nℹ {text}")
    else:
        print(f"\n{text}")


def display_error(text: str) -> None:
    """
    Display an error message.

    Args:
        text: Error message to display
    """
    display_message("error", text)
