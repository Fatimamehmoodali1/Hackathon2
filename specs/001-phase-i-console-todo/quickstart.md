# Quickstart Guide: Phase I Console Todo

**Version**: 1.0.0
**Phase**: I
**Last Updated**: 2025-12-28

## Prerequisites

- **Python**: 3.11 or higher ([Download](https://www.python.org/downloads/))
- **pip**: Python package installer (included with Python 3.11+)
- **Git**: For cloning repository ([Download](https://git-scm.com/downloads))
- **Terminal/Console**: Command-line interface (bash, zsh, PowerShell, cmd)

**Verify Prerequisites**:
```bash
python --version  # Should show Python 3.11.x or higher
pip --version     # Should show pip 23.x or higher
git --version     # Should show git 2.x or higher
```

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd phase1
```

### 2. Create a Virtual Environment

**On macOS/Linux**:
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows (PowerShell)**:
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt)**:
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Verify Activation**:
```bash
which python  # Should show path inside venv/ directory
# On Windows: where python
```

### 3. Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

**Expected Output**:
```
Successfully installed pytest-7.4.3 pytest-cov-4.1.0 black-23.12.1 pylint-3.0.3 mypy-1.7.1
```

**Note**: Phase I has no production dependencies (standard library only).

## Running the Application

From the repository root (with virtual environment activated):

```bash
python -m src.main
```

**Expected Output**:
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

**Stopping the Application**:
- Select menu option `7` to exit gracefully
- Or press `Ctrl+C` to force quit (may show Python traceback)

## Running Tests

### Run All Tests

```bash
pytest
```

**Expected Output**:
```
======================== test session starts =========================
collected 25 items

tests/unit/test_task.py .....                                  [ 20%]
tests/unit/test_task_service.py ..........                     [ 60%]
tests/unit/test_in_memory_repository.py .....                  [ 80%]
tests/integration/test_acceptance_scenarios.py .....           [100%]

========================= 25 passed in 0.50s =========================
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

**Expected Output**:
```
======================== test session starts =========================
collected 25 items

tests/unit/test_task.py .....                                  [ 20%]
...

---------- coverage: platform linux, python 3.11.7 -----------
Name                                  Stmts   Miss  Cover   Missing
-------------------------------------------------------------------
src/__init__.py                           0      0   100%
src/domain/__init__.py                    0      0   100%
src/domain/task.py                       15      0   100%
src/application/__init__.py               0      0   100%
src/application/task_service.py          45      2    96%   67-68
src/infrastructure/__init__.py            0      0   100%
src/infrastructure/in_memory_repo.py     25      0   100%
-------------------------------------------------------------------
TOTAL                                    85      2    98%
```

### Run Specific Test File

```bash
pytest tests/unit/test_task.py
```

### Run Tests Matching Pattern

```bash
pytest -k "add_task"  # Run all tests with "add_task" in name
```

### Run with Verbose Output

```bash
pytest -v  # Show each test name
```

### Run Acceptance Tests Only

```bash
pytest tests/integration/test_acceptance_scenarios.py -v
```

## Development Workflow

### 1. Test-Driven Development (TDD Red-Green-Refactor)

**Red: Write failing test**
```bash
# Edit tests/unit/test_task.py, add new test
pytest tests/unit/test_task.py::test_new_feature  # Should FAIL (RED)
```

**Green: Implement minimum code to pass**
```bash
# Edit src/domain/task.py, implement feature
pytest tests/unit/test_task.py::test_new_feature  # Should PASS (GREEN)
```

**Refactor: Improve code quality**
```bash
# Refactor code while keeping tests green
pytest  # All tests should still PASS
```

### 2. Code Quality Checks

**Run Linter** (catch errors and code smells):
```bash
pylint src/
```

**Run Type Checker** (static type analysis):
```bash
mypy src/
```

**Run Formatter** (consistent code style):
```bash
black src/ tests/  # Auto-format all code
```

**Check Formatting** (without modifying files):
```bash
black --check src/ tests/
```

### 3. Pre-Commit Checklist

Before committing code, run:
```bash
# 1. Format code
black src/ tests/

# 2. Run linter
pylint src/

# 3. Run type checker
mypy src/

# 4. Run all tests with coverage
pytest --cov=src --cov-report=term-missing

# 5. Verify acceptance scenarios
pytest tests/integration/test_acceptance_scenarios.py -v
```

All checks should pass before committing.

## Project Structure

```
phase1/
├── src/                          # Source code
│   ├── __init__.py
│   ├── main.py                   # Application entry point
│   ├── domain/                   # Business entities
│   │   ├── __init__.py
│   │   ├── task.py               # Task entity
│   │   └── task_repository.py   # Repository interface
│   ├── application/              # Business logic
│   │   ├── __init__.py
│   │   ├── task_service.py       # Task operations
│   │   └── errors.py             # Domain exceptions
│   ├── infrastructure/           # Storage implementation
│   │   ├── __init__.py
│   │   └── in_memory_repository.py  # In-memory storage
│   └── cli/                      # User interface
│       ├── __init__.py
│       ├── menu.py               # Main menu loop
│       ├── commands.py           # Command handlers
│       └── display.py            # Output formatting
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py               # Shared fixtures
│   ├── unit/                     # Unit tests
│   │   ├── test_task.py
│   │   ├── test_task_service.py
│   │   └── test_in_memory_repository.py
│   └── integration/              # Integration tests
│       ├── test_cli_workflows.py
│       └── test_acceptance_scenarios.py
├── specs/                        # Feature specifications
│   └── 001-phase-i-console-todo/
│       ├── spec.md               # Requirements
│       ├── plan.md               # Implementation plan
│       ├── data-model.md         # Domain model
│       ├── research.md           # Design decisions
│       ├── quickstart.md         # This file
│       └── contracts/            # Interface contracts
├── requirements.txt              # Production dependencies (empty)
├── requirements-dev.txt          # Development dependencies
└── README.md                     # Project overview
```

## Example Usage Session

```
=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete
6. Mark Incomplete
7. Exit

Enter your choice (1-7): 1

Enter task description: Buy groceries
✓ Task added successfully (ID: 1)

Enter your choice (1-7): 1

Enter task description: Call dentist
✓ Task added successfully (ID: 2)

Enter your choice (1-7): 1

Enter task description: Write report
✓ Task added successfully (ID: 3)

Enter your choice (1-7): 2

=== All Tasks ===
ID: 1 | Buy groceries | Status: Incomplete
ID: 2 | Call dentist | Status: Incomplete
ID: 3 | Write report | Status: Incomplete

Enter your choice (1-7): 5

Enter task ID to mark complete: 1
✓ Task marked complete (ID: 1)

Enter your choice (1-7): 2

=== All Tasks ===
ID: 1 | Buy groceries | Status: Complete
ID: 2 | Call dentist | Status: Incomplete
ID: 3 | Write report | Status: Incomplete

Enter your choice (1-7): 3

Enter task ID to update: 2
Enter new task description: Call dentist at 3pm
✓ Task updated successfully (ID: 2)

Enter your choice (1-7): 4

Enter task ID to delete: 3
✓ Task deleted successfully (ID: 3)

Enter your choice (1-7): 2

=== All Tasks ===
ID: 1 | Buy groceries | Status: Complete
ID: 2 | Call dentist at 3pm | Status: Incomplete

Enter your choice (1-7): 7

Goodbye!
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'src'`

**Cause**: Running from wrong directory or incorrect Python path

**Solution**:
```bash
# Ensure you're in the repository root
pwd  # Should show .../phase1

# Run with module syntax (not direct file execution)
python -m src.main  # Correct
python src/main.py  # Incorrect (may fail)
```

### Issue: Tests fail with import errors

**Cause**: Virtual environment not activated or dependencies not installed

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\Activate.ps1  # Windows PowerShell

# Reinstall dependencies
pip install -r requirements-dev.txt

# Verify pytest is installed
pytest --version
```

### Issue: Application doesn't exit

**Cause**: Stuck in input prompt or infinite loop

**Solution**:
- Use menu option 7 to exit gracefully
- Press `Ctrl+C` to force quit (keyboard interrupt)
- Close terminal window as last resort

### Issue: `TypeError: unsupported operand type(s)`

**Cause**: Invalid input (non-numeric ID, wrong data type)

**Solution**: The application validates input; if you see this error, it's a bug. Please:
1. Note the exact steps to reproduce
2. Run tests to verify: `pytest -v`
3. Report issue if tests pass but app fails

### Issue: Coverage below 90%

**Cause**: Untested code paths

**Solution**:
```bash
# Identify missing coverage
pytest --cov=src --cov-report=term-missing

# Look for "Missing" column, add tests for those lines
# Example: Missing lines 67-68 in task_service.py
```

## Performance Expectations

Based on specification success criteria:

| Operation | Expected Performance | Actual (typical) |
|-----------|---------------------|------------------|
| Add task | < 5 seconds | < 0.01 seconds |
| View tasks (100 tasks) | < 1 second | < 0.05 seconds |
| Update task | < 5 seconds | < 0.01 seconds |
| Delete task | < 5 seconds | < 0.01 seconds |
| Mark complete/incomplete | < 5 seconds | < 0.01 seconds |

All operations complete well under specification limits.

## Next Steps

### After Phase I Completion

1. **Verify Acceptance Criteria**:
   ```bash
   pytest tests/integration/test_acceptance_scenarios.py -v
   ```
   All 13 scenarios should pass.

2. **Confirm Success Criteria**:
   - [ ] SC-001: Operations complete within 5 seconds ✅
   - [ ] SC-002: No unclear error messages ✅
   - [ ] SC-003: Valid inputs succeed ✅
   - [ ] SC-004: Invalid inputs show clear errors ✅
   - [ ] SC-005: Handle 100 tasks without degradation ✅
   - [ ] SC-006: Menu self-explanatory ✅
   - [ ] SC-007: IDs never reused ✅

3. **Move to Next Phase**:
   - Phase II: Web interface (FastAPI backend + frontend)
   - Phase III: Database persistence (SQLModel + Neon DB)
   - Phase IV: Multi-user support (authentication, authorization)
   - Phase V: Advanced features (priorities, due dates, categories)

### Resources

- **Specification**: `specs/001-phase-i-console-todo/spec.md`
- **Implementation Plan**: `specs/001-phase-i-console-todo/plan.md`
- **Data Model**: `specs/001-phase-i-console-todo/data-model.md`
- **Research**: `specs/001-phase-i-console-todo/research.md`
- **Contracts**: `specs/001-phase-i-console-todo/contracts/`

## Support

For issues or questions:
1. Check this quickstart guide
2. Review specification and plan documents
3. Run tests to diagnose: `pytest -v`
4. Check console error messages
5. Report bugs with reproduction steps

---

**Happy Coding!** 🚀
