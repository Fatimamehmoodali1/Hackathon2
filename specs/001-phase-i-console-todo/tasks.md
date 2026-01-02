# Tasks: Phase I Console Todo Application

**Input**: Design documents from `/specs/001-phase-i-console-todo/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, contracts/, quickstart.md

**Tests**: Tests are OPTIONAL - include based on TDD approach from research.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- Single project structure: `src/`, `tests/` at repository root
- Paths follow Clean Architecture: `src/domain/`, `src/application/`, `src/infrastructure/`, `src/cli/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

**References**: plan.md (Project Structure), quickstart.md (Installation)

- [X] T001 Create src/ directory structure with subdirectories: domain/, application/, infrastructure/, cli/ at repository root
- [X] T002 Create tests/ directory structure with subdirectories: unit/, integration/ at repository root
- [X] T003 [P] Create requirements.txt with empty content (no production dependencies for Phase I)
- [X] T004 [P] Create requirements-dev.txt with: pytest==7.4.3, pytest-cov==4.1.0, black==23.12.1, pylint==3.0.3, mypy==1.7.1
- [X] T005 [P] Create __init__.py files in all src/ subdirectories (domain, application, infrastructure, cli)
- [X] T006 [P] Create __init__.py files in all tests/ subdirectories (unit, integration, root)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**References**: data-model.md (Domain Entities), research.md (Error Handling), contracts/

- [X] T007 Create domain exceptions in src/application/errors.py: TodoError (base), TaskNotFoundError, InvalidTaskIdError, EmptyDescriptionError
- [X] T008 Create Task entity dataclass in src/domain/task.py with id (int), description (str), is_complete (bool, default=False) and __post_init__ validation
- [X] T009 Create TaskRepository abstract interface in src/domain/task_repository.py with methods: add, get, get_all, update, delete, exists, get_next_id (per contracts/task_repository_interface.py)
- [X] T010 Create InMemoryTaskRepository in src/infrastructure/in_memory_repository.py implementing TaskRepository with dict[int, Task] storage and _next_id counter (per data-model.md, research.md)
- [X] T011 Create TaskService in src/application/task_service.py with all CRUD methods: add_task, get_task, get_all_tasks, update_task, delete_task, mark_complete, mark_incomplete (per contracts/task_service_interface.py)
- [X] T012 Create main entry point in src/main.py with application initialization and main() function placeholder

**Checkpoint**: Foundation ready - domain layer, repository, and service layer complete. User story implementation can now begin.

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add new tasks and view all tasks in the list

**Independent Test**: Launch application, add 2-3 tasks with different descriptions, view the list to confirm all tasks appear with correct details

**References**: spec.md (User Story 1, FR-001, FR-002, FR-003, FR-009, SC-001), data-model.md (CLI Presentation Layer)

### Implementation for User Story 1

- [X] T013 [P] [US1] Create display utilities in src/cli/display.py with functions: display_menu(), display_tasks(tasks), display_message(msg_type, text), display_error(text)
- [X] T014 [P] [US1] Create input validation in src/cli/validation.py with functions: validate_menu_choice(choice) -> (bool, int | str), validate_task_id(input_str) -> (bool, int | str), validate_description(desc) -> (bool, str) (per research.md)
- [X] T015 [US1] Create command handler for add_task in src/cli/commands.py: handle_add_task(service) that prompts for description, validates, calls service.add_task(), and displays result
- [X] T016 [US1] Create command handler for view_tasks in src/cli/commands.py: handle_view_tasks(service) that calls service.get_all_tasks() and displays formatted list or "No tasks found" message
- [X] T017 [US1] Create main menu loop in src/cli/menu.py: main_menu(service) that displays menu, captures input, validates choice, routes to commands, and loops until exit option selected (per data-model.md CLI Presentation Layer)
- [X] T018 [US1] Update src/main.py to initialize InMemoryTaskRepository, TaskService, and call main_menu() to start the application
- [X] T019 [US1] Test add task workflow: Verify description validation (reject empty/whitespace), ID assignment starts at 1 and increments, confirmation message displays
- [X] T020 [US1] Test view tasks workflow: Verify empty list shows "No tasks found", non-empty list shows all tasks with ID, description, status (Incomplete by default)
- [X] T021 [US1] Verify menu navigation: Invalid menu choices show error and redisplay menu, option 7 (Exit) terminates application cleanly

**Checkpoint**: At this point, User Story 1 should be fully functional. Users can add and view tasks independently.

---

## Phase 4: User Story 2 - Mark Tasks Complete/Incomplete (Priority: P2)

**Goal**: Users can mark tasks as complete or incomplete to track progress

**Independent Test**: Add tasks, mark some complete, view updated status, toggle them back to incomplete

**References**: spec.md (User Story 2, FR-009, FR-010), plan.md (TaskService methods)

### Implementation for User Story 2

- [X] T022 [US2] Create command handler for mark_complete in src/cli/commands.py: handle_mark_complete(service) that prompts for task ID, validates numeric input, calls service.mark_complete(), and displays success or TaskNotFoundError
- [X] T023 [US2] Create command handler for mark_incomplete in src/cli/commands.py: handle_mark_incomplete(service) that prompts for task ID, validates numeric input, calls service.mark_incomplete(), and displays success or TaskNotFoundError
- [X] T024 [US2] Update src/cli/menu.py display_menu() to include options "5. Mark Complete" and "6. Mark Incomplete" in the menu text
- [X] T025 [US2] Update src/cli/menu.py main_menu() to route choice 5 to handle_mark_complete() and choice 6 to handle_mark_incomplete()
- [X] T026 [US2] Test mark complete workflow: Add incomplete task, mark it complete, view list to verify status changed to "Complete", try marking non-existent task ID, verify TaskNotFoundError displays
- [X] T027 [US2] Test mark incomplete workflow: Mark complete task as incomplete, view list to verify status changed back to "Incomplete"
- [X] T028 [US2] Test invalid ID handling: Enter non-numeric ID, verify "Invalid task ID format" error displays

**Checkpoint**: At this point, User Story 2 works independently. Users can toggle task completion status.

---

## Phase 5: User Story 3 - Update Task Description (Priority: P3)

**Goal**: Users can update the description of existing tasks

**Independent Test**: Add a task, update its description, view the task to confirm the change

**References**: spec.md (User Story 3, FR-005, FR-008)

### Implementation for User Story 3

- [X] T029 [US3] Create command handler for update_task in src/cli/commands.py: handle_update_task(service) that prompts for task ID, validates numeric input, prompts for new description, validates non-empty, calls service.update_task(), and displays success or errors
- [X] T030 [US3] Update src/cli/menu.py display_menu() to include "3. Update Task" option in the menu text
- [X] T031 [US3] Update src/cli/menu.py main_menu() to route choice 3 to handle_update_task()
- [X] T032 [US3] Test update task workflow: Add task, update its description, view list to verify new description appears
- [X] T033 [US3] Test update with invalid ID: Enter non-existent task ID, verify TaskNotFoundError displays
- [X] T034 [US3] Test update with empty description: Enter empty or whitespace-only description, verify EmptyDescriptionError or validation error displays

**Checkpoint**: At this point, User Story 3 works independently. Users can edit task descriptions.

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Users can delete tasks that are no longer relevant

**Independent Test**: Add tasks, delete specific ones by ID, view the list to confirm they're removed

**References**: spec.md (User Story 4, FR-012)

### Implementation for User Story 4

- [X] T035 [US4] Create command handler for delete_task in src/cli/commands.py: handle_delete_task(service) that prompts for task ID, validates numeric input, calls service.delete_task(), and displays success or TaskNotFoundError
- [X] T036 [US4] Update src/cli/menu.py display_menu() to include "4. Delete Task" option in the menu text
- [X] T037 [US4] Update src/cli/menu.py main_menu() to route choice 4 to handle_delete_task()
- [X] T038 [US4] Test delete task workflow: Add 3 tasks, delete task ID 2, view list to verify only tasks 1 and 3 remain (IDs never reused)
- [X] T039 [US4] Test delete non-existent task: Enter non-existent task ID, verify TaskNotFoundError displays
- [X] T040 [US4] Test delete with invalid ID: Enter non-numeric ID, verify validation error displays

**Checkpoint**: At this point, User Story 4 works independently. Users can delete tasks and list remains clean.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

**References**: spec.md (Success Criteria, Edge Cases), plan.md (Success Validation)

- [X] T041 Test long descriptions: Add task with 1000+ character description, verify system accepts and displays without truncation (spec.md edge case)
- [X] T042 Test special characters and unicode: Add tasks with unicode characters (e.g., "Café ☕", emojis) and special characters, verify system handles and displays correctly (spec.md edge case)
- [X] T043 Test rapid task addition: Quickly add multiple tasks, verify correct ID sequencing (1, 2, 3, ...) maintained (spec.md edge case)
- [X] T044 Test ID reuse prevention: Add tasks, delete some, add more, verify IDs continue incrementing and never reuse deleted IDs (spec.md edge case, SC-007)
- [X] T045 Test performance with 100 tasks: Add 100 tasks, verify view_tasks completes within 1 second (spec.md SC-005)
- [X] T046 Verify all FR requirements: Confirm all 12 functional requirements (FR-001 through FR-012) from spec.md are implemented
- [X] T047 Verify all success criteria: Confirm all 7 success criteria (SC-001 through SC-007) from spec.md are met
- [X] T048 [P] Run code quality tools: black --check src/ tests/, mypy src/, pylint src/ to ensure constitutional quality standards
- [X] T049 [P] Run test coverage: pytest --cov=src --cov-report=term-missing, verify >90% coverage for domain and application layers (per research.md)
- [X] T050 Run quickstart.md validation: Follow all steps in quickstart.md to verify setup, running, and testing work as documented
- [X] T051 [P] Create README.md at repository root with project overview, installation instructions, and usage example (derived from quickstart.md)

**Final Checkpoint**: All user stories complete, edge cases handled, success criteria met, code quality verified.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on Foundational (Phase 2) - Uses same service/repository, no dependency on US1
- **User Story 3 (P3)**: Depends on Foundational (Phase 2) - Uses same service/repository, no dependency on US1/US2
- **User Story 4 (P4)**: Depends on Foundational (Phase 2) - Uses same service/repository, no dependency on US1/US2/US3

### Within Each User Story

- **US1**: Display utilities (T013) and validation (T014) are parallel [P]; command handlers (T015, T016) can be parallel; menu integration (T017) depends on commands; main.py (T018) depends on menu
- **US2**: Command handlers (T022, T023) are parallel [P]; menu updates (T024, T025) depend on commands
- **US3**: Command handler (T029) then menu updates (T030, T031)
- **US4**: Command handler (T035) then menu updates (T036, T037)

### Parallel Opportunities

- **Setup Phase (T003, T004, T005, T006)**: All [P] - can run in parallel (different files)
- **Foundational Phase**: Sequential due to dependencies (errors → task entity → repository interface → repository → service)
- **US1**: T013 [P] and T014 [P] can run in parallel
- **US2**: T022 [P] and T023 [P] can run in parallel
- **US3**: No parallel tasks (single command handler)
- **US4**: No parallel tasks (single command handler)
- **Polish Phase**: T041-T046 are sequential tests; T048 [P], T049 [P], T050 [P], T051 [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Phase 1-2 must complete first

# Launch all parallel tasks for US1 together:
Task: T013 [P] [US1] Create display utilities in src/cli/display.py
Task: T014 [P] [US1] Create input validation in src/cli/validation.py

# After T013 and T014 complete, run command handlers in parallel:
Task: T015 [US1] Create command handler for add_task in src/cli/commands.py
Task: T016 [US1] Create command handler for view_tasks in src/cli/commands.py

# After T015 and T016 complete, continue with sequential:
Task: T017 [US1] Create main menu loop in src/cli/menu.py
Task: T018 [US1] Update src/main.py
Task: T019-T021: Test workflow
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. **Complete Phase 1: Setup** (T001-T006) - Project structure and requirements
2. **Complete Phase 2: Foundational** (T007-T012) - Domain layer and service infrastructure
3. **Complete Phase 3: User Story 1** (T013-T021) - Add and view tasks
4. **STOP and VALIDATE**: Test User Story 1 independently per spec.md User Story 1 Independent Test criteria
5. Deploy/demo MVP if ready

### Incremental Delivery

1. **Setup + Foundational** (T001-T012) → Foundation ready, all infrastructure complete
2. **Add User Story 1** (T013-T021) → Test independently → Deploy/Demo MVP
3. **Add User Story 2** (T022-T028) → Test independently → Deploy/Demo
4. **Add User Story 3** (T029-T034) → Test independently → Deploy/Demo
5. **Add User Story 4** (T035-T040) → Test independently → Deploy/Demo
6. **Polish Phase** (T041-T051) → Final validation and quality checks
7. Each story adds value without breaking previous stories

### Sequential Execution (Single Developer)

1. T001-T006: Setup
2. T007-T012: Foundational (BLOCKS all stories until complete)
3. T013-T021: User Story 1 (P1)
4. T022-T028: User Story 2 (P2)
5. T029-T034: User Story 3 (P3)
6. T035-T040: User Story 4 (P4)
7. T041-T051: Polish

---

## Notes

- **[P] tasks** = different files, no dependencies, safe to run in parallel
- **[Story] label** = maps task to specific user story for traceability
- Each user story is independently completable and testable
- User stories share common infrastructure (repository, service) but don't depend on each other's implementation
- All tasks reference specific files and follow Clean Architecture structure
- Task descriptions include sufficient detail for LLM execution without additional context
- Exit option (7) in menu handled from User Story 1 (T017 menu loop)
- Avoid: vague tasks ("implement feature"), same file conflicts in parallel tasks, cross-story dependencies that break independence
