"""Command handlers for CLI menu options"""
from src.application.task_service import TaskService
from src.application.errors import TaskNotFoundError, EmptyDescriptionError
from .validation import validate_task_id, validate_description
from .display import display_message, display_error, display_tasks


def handle_add_task(service: TaskService) -> None:
    """
    Handle add task command.

    Args:
        service: TaskService instance
    """
    description = input("\nEnter task description: ")
    is_valid, result = validate_description(description)

    if not is_valid:
        display_error(result)
        return

    try:
        task = service.add_task(result)
        display_message("success", f"Task added successfully (ID: {task.id})")
    except EmptyDescriptionError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to add task: {str(e)}")


def handle_view_tasks(service: TaskService) -> None:
    """
    Handle view tasks command.

    Args:
        service: TaskService instance
    """
    try:
        tasks = service.get_all_tasks()
        display_tasks(tasks)
    except Exception as e:
        display_error(f"Failed to retrieve tasks: {str(e)}")


def handle_update_task(service: TaskService) -> None:
    """
    Handle update task command.

    Args:
        service: TaskService instance
    """
    task_id_input = input("\nEnter task ID to update: ")
    is_valid, result = validate_task_id(task_id_input)

    if not is_valid:
        display_error(result)
        return

    task_id = result
    new_description = input("Enter new task description: ")
    is_valid, result = validate_description(new_description)

    if not is_valid:
        display_error(result)
        return

    try:
        task = service.update_task(task_id, result)
        display_message("success", f"Task updated successfully (ID: {task.id})")
    except TaskNotFoundError as e:
        display_error(str(e))
    except EmptyDescriptionError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to update task: {str(e)}")


def handle_delete_task(service: TaskService) -> None:
    """
    Handle delete task command.

    Args:
        service: TaskService instance
    """
    task_id_input = input("\nEnter task ID to delete: ")
    is_valid, result = validate_task_id(task_id_input)

    if not is_valid:
        display_error(result)
        return

    task_id = result

    try:
        service.delete_task(task_id)
        display_message("success", f"Task deleted successfully (ID: {task_id})")
    except TaskNotFoundError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to delete task: {str(e)}")


def handle_mark_complete(service: TaskService) -> None:
    """
    Handle mark complete command.

    Args:
        service: TaskService instance
    """
    task_id_input = input("\nEnter task ID to mark complete: ")
    is_valid, result = validate_task_id(task_id_input)

    if not is_valid:
        display_error(result)
        return

    task_id = result

    try:
        task = service.mark_complete(task_id)
        display_message("success", f"Task marked complete (ID: {task.id})")
    except TaskNotFoundError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to mark task complete: {str(e)}")


def handle_mark_incomplete(service: TaskService) -> None:
    """
    Handle mark incomplete command.

    Args:
        service: TaskService instance
    """
    task_id_input = input("\nEnter task ID to mark incomplete: ")
    is_valid, result = validate_task_id(task_id_input)

    if not is_valid:
        display_error(result)
        return

    task_id = result

    try:
        task = service.mark_incomplete(task_id)
        display_message("success", f"Task marked incomplete (ID: {task.id})")
    except TaskNotFoundError as e:
        display_error(str(e))
    except Exception as e:
        display_error(f"Failed to mark task incomplete: {str(e)}")
