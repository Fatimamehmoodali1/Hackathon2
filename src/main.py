"""Main entry point for Phase I Console Todo Application"""
from src.infrastructure.in_memory_repository import InMemoryTaskRepository
from src.application.task_service import TaskService
from src.cli.menu import main_menu


def main():
    """Initialize application and start main menu loop."""
    # Initialize repository and service
    repository = InMemoryTaskRepository()
    service = TaskService(repository)

    # Start the CLI menu
    main_menu(service)


if __name__ == "__main__":
    main()
