"""Input validation utilities for CLI"""
from typing import Tuple, Union


def validate_menu_choice(choice: str) -> Tuple[bool, Union[int, str]]:
    """
    Validate menu choice input.

    Args:
        choice: User input string

    Returns:
        (True, choice_number) if valid, (False, error_message) if invalid
    """
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= 7:
            return True, choice_num
        else:
            return False, "Please enter a number between 1 and 7"
    except ValueError:
        return False, "Invalid input. Please enter a number between 1 and 7"


def validate_task_id(input_str: str) -> Tuple[bool, Union[int, str]]:
    """
    Validate task ID input.

    Args:
        input_str: User input string

    Returns:
        (True, task_id) if valid, (False, error_message) if invalid
    """
    try:
        task_id = int(input_str)
        if task_id <= 0:
            return False, "Task ID must be a positive number"
        return True, task_id
    except ValueError:
        return False, "Invalid task ID format. Please enter a number"


def validate_description(description: str) -> Tuple[bool, str]:
    """
    Validate task description input.

    Args:
        description: User input string

    Returns:
        (True, description) if valid, (False, error_message) if invalid
    """
    stripped = description.strip()
    if not stripped:
        return False, "Task description cannot be empty"
    return True, stripped
