# Phase I Console Todo Application

A simple, in-memory command-line todo application built with Python 3.11+.

## Features

- ✅ Add new tasks
- ✅ View all tasks
- ✅ Update task descriptions
- ✅ Delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Clean menu-driven interface
- ✅ Input validation and error handling

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd phase1
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install development dependencies** (optional, for testing):
   ```bash
   pip install -r requirements-dev.txt
   ```

## Running the Application

From the repository root:

```bash
python -m src.main
```

You should see the main menu:

```
=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete
6. Mark Incomplete
7. Exit

Enter your choice (1-7):
```

## Usage Example

```
Enter your choice (1-7): 1

Enter task description: Buy groceries
✓ Task added successfully (ID: 1)

Enter your choice (1-7): 1

Enter task description: Call dentist
✓ Task added successfully (ID: 2)

Enter your choice (1-7): 2

=== All Tasks ===
ID: 1 | Buy groceries | Status: Incomplete
ID: 2 | Call dentist | Status: Incomplete

Enter your choice (1-7): 5

Enter task ID to mark complete: 1
✓ Task marked complete (ID: 1)

Enter your choice (1-7): 2

=== All Tasks ===
ID: 1 | Buy groceries | Status: Complete
ID: 2 | Call dentist | Status: Incomplete

Enter your choice (1-7): 7

Goodbye!
```

## Architecture

The application follows Clean Architecture principles:

- **Domain Layer** (`src/domain/`): Business entities (Task) and interfaces (TaskRepository)
- **Application Layer** (`src/application/`): Business logic (TaskService) and domain exceptions
- **Infrastructure Layer** (`src/infrastructure/`): In-memory storage implementation
- **CLI Layer** (`src/cli/`): User interface, menu, commands, and display utilities

## Project Structure

```
phase1/
├── src/
│   ├── domain/          # Business entities
│   │   ├── task.py
│   │   └── task_repository.py
│   ├── application/     # Business logic
│   │   ├── task_service.py
│   │   └── errors.py
│   ├── infrastructure/  # Storage implementation
│   │   └── in_memory_repository.py
│   └── cli/             # User interface
│       ├── menu.py
│       ├── commands.py
│       ├── display.py
│       └── validation.py
├── tests/
│   ├── unit/
│   └── integration/
├── specs/               # Feature specifications
├── requirements.txt     # Production dependencies (none)
└── requirements-dev.txt # Development dependencies
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_task.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Type checking
mypy src/

# Linting
pylint src/
```

## Important Notes

- **In-memory only**: All data is stored in memory and lost when the application exits
- **Single user**: Designed for one user at a time
- **No persistence**: No database or file storage in Phase I
- **Task IDs**: Sequential integers starting from 1, never reused

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'src'`
- **Solution**: Run from repository root with `python -m src.main`, not `python src/main.py`

**Issue**: Application doesn't exit
- **Solution**: Select menu option 7 or press `Ctrl+C`

## Next Phases

- **Phase II**: Web interface with FastAPI
- **Phase III**: Database persistence with SQLModel + Neon DB
- **Phase IV**: Multi-user support with authentication
- **Phase V**: Advanced features (priorities, due dates, categories)

## License

This is an educational project for learning software development principles.

---

**Version**: Phase I
**Status**: Complete ✅
**Tech Stack**: Python 3.11+, Standard Library Only
