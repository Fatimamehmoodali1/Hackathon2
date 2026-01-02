"""Main menu loop for CLI"""
from src.application.task_service import TaskService
from .display import display_menu, display_error
from .validation import validate_menu_choice
from .commands import (
    handle_add_task,
    handle_view_tasks,
    handle_update_task,
    handle_delete_task,
    handle_mark_complete,
    handle_mark_incomplete,
)


def main_menu(service: TaskService) -> None:
    """
    Main menu loop - displays menu, captures input, routes to commands.

    Args:
        service: TaskService instance
    """
    while True:
        display_menu()
        choice_input = input("\nEnter your choice (1-7): ")

        is_valid, result = validate_menu_choice(choice_input)

        if not is_valid:
            display_error(result)
            continue

        choice = result

        if choice == 1:
            handle_add_task(service)
        elif choice == 2:
            handle_view_tasks(service)
        elif choice == 3:
            handle_update_task(service)
        elif choice == 4:
            handle_delete_task(service)
        elif choice == 5:
            handle_mark_complete(service)
        elif choice == 6:
            handle_mark_incomplete(service)
        elif choice == 7:
            print("\nGoodbye!")
            break
