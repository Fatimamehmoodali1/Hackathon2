---
description: "Phase II Full-Stack Todo Application - Implementation Tasks"
---

# Tasks: Phase II - Full-Stack Todo Application

**Input**: Design documents from `/specs/001-phase-2-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/
**Tests**: Tests included for TDD approach

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`
- **Specs**: `specs/001-phase-2-todo-app/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both backend and frontend

### Backend Setup

- [ ] T001 Create backend directory structure per plan.md: backend/src/{models,services,api,schemas,core}, backend/tests/{unit,integration}
- [ ] T002 Initialize Python virtual environment and create requirements.txt with FastAPI, SQLModel, Better Auth, uvicorn, alembic, psycopg
- [ ] T003 [P] Configure pyproject.toml with Python 3.11+, dependencies, and scripts
- [ ] T004 [P] Configure ruff, black, and mypy for backend linting and formatting
- [ ] T005 [P] Create .env.example with DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS variables

### Frontend Setup

- [ ] T006 Create frontend directory structure per plan.md: frontend/src/{app,components,lib,styles}, frontend/tests/e2e
- [ ] T007 Initialize Next.js 14 project with TypeScript, Tailwind CSS (optional), and App Router
- [ ] T008 [P] Configure package.json with dependencies, scripts, and TypeScript settings in tsconfig.json
- [ ] T009 [P] Configure next.config.js for API proxy to backend
- [ ] T010 [P] Create .env.local.example with NEXT_PUBLIC_API_URL variable

**Checkpoint**: Both projects initialized with basic structure and configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Database Foundation

- [ ] T011 Create backend/src/core/config.py with Config class loading environment variables
- [ ] T012 Create backend/src/core/database.py with async database connection using SQLModel and Neon PostgreSQL
- [ ] T013 [P] Create backend/src/models/__init__.py to export all models
- [ ] T014 Create backend/src/models/user.py with User SQLModel entity (id, email, password_hash, created_at)
- [ ] T015 [P] Create backend/src/models/todo.py with Todo SQLModel entity (id, user_id, title, is_complete, created_at, updated_at)
- [ ] T016 Create alembic.ini and backend/alembic/ directory for migrations
- [ ] T017 [P] Create backend/alembic/env.py for SQLModel + Alembic integration
- [ ] T018 Generate and run initial migration to create users and todos tables

### Backend Core Infrastructure

- [ ] T019 Create backend/src/schemas/__init__.py to export all Pydantic schemas
- [ ] T020 Create backend/src/schemas/user.py with UserCreate, UserResponse, UserLogin schemas
- [ ] T021 [P] Create backend/src/schemas/todo.py with TodoCreate, TodoUpdate, TodoResponse, TodoListResponse schemas
- [ ] T022 Create backend/src/core/auth.py with Better Auth configuration and session management
- [ ] T023 [P] Create backend/src/api/__init__.py to export all routers
- [ ] T024 Create backend/src/main.py with FastAPI app initialization, CORS configuration, and included routers
- [ ] T025 Configure backend error handling in backend/src/api/middleware/error_handler.py with proper HTTP status codes and JSON error responses

### Frontend Foundation

- [ ] T026 Create frontend/src/lib/__init__.py and frontend/src/lib/api.ts with API client wrapper (get, post, put, patch, delete)
- [ ] T027 [P] Create frontend/src/lib/auth.tsx with AuthContext for managing authentication state
- [ ] T028 Create frontend/src/styles/globals.css with base responsive styles
- [ ] T029 Create frontend/src/app/layout.tsx with AuthProvider wrapper and global layout

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: Allow new users to create an account with email and password

**Independent Test**: Complete signup form with valid input, verify user account exists in database, confirm redirect to signin page

### Backend Implementation (User Registration)

- [ ] T030 [P] [US1] Create backend/src/services/auth_service.py with UserService class for registration logic
- [ ] T031 [P] [US1] Create backend/src/api/auth/signup.py POST endpoint with Better Auth signup, input validation, error handling
- [ ] T032 [US1] Implement password hashing using bcrypt in auth_service.py
- [ ] T033 [US1] Add email uniqueness validation and conflict error handling

### Frontend Implementation (User Registration)

- [ ] T034 [P] [US1] Create frontend/src/app/(auth)/signup/page.tsx with signup form (email, password fields)
- [ ] T035 [US1] Implement form validation for email format and minimum password length
- [ ] T036 [US1] Connect form to API client, handle success redirect to /signin, display validation errors inline

**Checkpoint**: User Story 1 complete - users can register and accounts are persisted

---

## Phase 4: User Story 2 - User Sign In (Priority: P1)

**Goal**: Allow registered users to authenticate and access their personal todo list

**Independent Test**: Complete signin form with correct credentials, verify session established, confirm redirect to todos page

### Backend Implementation (User Sign In)

- [ ] T037 [P] [US2] Create backend/src/api/auth/signin.py POST endpoint with Better Auth signin
- [ ] T038 [P] [US2] Create backend/src/api/auth/signout.py POST endpoint for ending session
- [ ] T039 [P] [US2] Create backend/src/api/auth/me.py GET endpoint for current user info
- [ ] T040 [US2] Implement credential validation with bcrypt password comparison
- [ ] T041 [US2] Add generic error message for invalid credentials (prevent email enumeration)

### Frontend Implementation (User Sign In)

- [ ] T042 [P] [US2] Create frontend/src/app/(auth)/signin/page.tsx with signin form (email, password fields)
- [ ] T043 [US2] Connect form to API client, handle success redirect to /todos, display error message on failure
- [ ] T044 [P] [US2] Update AuthContext to handle session cookie and user state from /auth/me endpoint
- [ ] T045 [US2] Create frontend/src/middleware.ts for Next.js to check auth cookie and redirect to /signin if not authenticated

**Checkpoint**: User Story 2 complete - users can sign in and access protected pages

---

## Phase 5: User Story 3 - View Todos (Priority: P1)

**Goal**: Display all todos belonging to the authenticated user

**Independent Test**: Sign in, navigate to /todos, verify all user's todos are displayed with title, completion status, and visual distinction

### Backend Implementation (View Todos)

- [ ] T046 [P] [US3] Create backend/src/services/todo_service.py with TodoService class for CRUD operations
- [ ] T047 [P] [US3] Create backend/src/api/todos/__init__.py router with authentication dependency
- [ ] T048 [US3] Implement GET /api/todos endpoint to fetch all todos for authenticated user with user_id filter
- [ ] T049 [US3] Add GET /api/todos/:id endpoint for single todo retrieval with ownership check

### Frontend Implementation (View Todos)

- [ ] T050 [P] [US3] Create frontend/src/app/todos/layout.tsx with protected route wrapper
- [ ] T051 [US3] Create frontend/src/app/todos/page.tsx with todo list display
- [ ] T052 [P] [US3] Create frontend/src/components/TodoList.tsx for rendering list of todos
- [ ] T053 [P] [US3] Create frontend/src/components/TodoItem.tsx for individual todo display with visual completion status
- [ ] T054 [US3] Implement empty state message when user has no todos
- [ ] T055 [US3] Fetch todos from API on page load, handle loading and error states

**Checkpoint**: User Story 3 complete - users can view their todo list

---

## Phase 6: User Story 4 - Create Todo (Priority: P1)

**Goal**: Allow authenticated users to add new todos to their list

**Independent Test**: Sign in, enter todo title, submit, verify new todo appears in list with incomplete status

### Backend Implementation (Create Todo)

- [ ] T056 [P] [US4] Create POST /api/todos endpoint with title validation (1-200 chars), user_id from session
- [ ] T057 [US4] Implement todo creation in todo_service.py with created_at timestamp

### Frontend Implementation (Create Todo)

- [ ] T058 [P] [US4] Create frontend/src/components/TodoInput.tsx with text input and add button
- [ ] T059 [US4] Connect input to API POST /todos, add new todo to list optimistically, display validation error on failure
- [ ] T060 [US4] Clear input after successful creation, show loading state during API call

**Checkpoint**: User Story 4 complete - users can create new todos

---

## Phase 7: User Story 5 - Edit Todo (Priority: P2)

**Goal**: Allow authenticated users to update their existing todo titles

**Independent Test**: Click edit on todo, modify title, save, verify change reflected in todo list

### Backend Implementation (Edit Todo)

- [ ] T061 [P] [US5] Create PUT /api/todos/:id endpoint with title validation
- [ ] T062 [US5] Implement update logic in todo_service.py with updated_at timestamp
- [ ] T063 [US5] Add ownership verification to prevent editing other users' todos (return 403)

### Frontend Implementation (Edit Todo)

- [ ] T064 [P] [US5] Add edit mode to TodoItem.tsx with inline title editing or modal
- [ ] T065 [US5] Connect edit to API PUT /todos/:id, update todo in list on success, show error on failure
- [ ] T066 [US5] Implement cancel edit without changes, show validation errors

**Checkpoint**: User Story 5 complete - users can edit their todos

---

## Phase 8: User Story 6 - Delete Todo (Priority: P2)

**Goal**: Allow authenticated users to remove todos from their list

**Independent Test**: Click delete on todo, confirm dialog, verify todo no longer appears in list

### Backend Implementation (Delete Todo)

- [ ] T067 [P] [US6] Create DELETE /api/todos/:id endpoint
- [ ] T068 [US6] Implement hard delete in todo_service.py with CASCADE verification
- [ ] T069 [US6] Add ownership verification to prevent deleting other users' todos (return 403)

### Frontend Implementation (Delete Todo)

- [ ] T070 [P] [US6] Create frontend/src/components/Modal.tsx for confirmation dialog
- [ ] T071 [US6] Add delete button to TodoItem.tsx with confirmation dialog
- [ ] T072 [US6] Connect delete to API DELETE /todos/:id, remove todo from list on success, show error on failure

**Checkpoint**: User Story 6 complete - users can delete their todos

---

## Phase 9: User Story 7 - Toggle Todo Completion (Priority: P1)

**Goal**: Allow authenticated users to mark todos as complete or incomplete

**Independent Test**: Click toggle on todo, verify visual appearance changes to indicate completion status, verify change persists

### Backend Implementation (Toggle Completion)

- [ ] T073 [P] [US7] Create PATCH /api/todos/:id/toggle endpoint with is_complete in request body
- [ ] T074 [US7] Implement toggle logic in todo_service.py with updated_at timestamp
- [ ] T075 [US7] Add ownership verification to prevent toggling other users' todos (return 403)

### Frontend Implementation (Toggle Completion)

- [ ] T076 [P] [US7] Add toggle checkbox/button to TodoItem.tsx
- [ ] T077 [US7] Connect toggle to API PATCH /todos/:id/toggle, update todo visual appearance on success, revert on error

**Checkpoint**: User Story 7 complete - users can toggle todo completion

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Responsive Design

- [ ] T078 [P] Review and update all frontend components for mobile responsiveness (minimum 44px touch targets)
- [ ] T079 [P] Ensure todo list displays correctly on mobile with single-column layout
- [ ] T080 [P] Test and fix any responsive issues on auth pages

### Error Handling Polish

- [ ] T081 [P] Review backend error responses for consistency across all endpoints
- [ ] T082 [P] Ensure frontend displays user-friendly error messages for all error types
- [ ] T083 [P] Add network failure handling with retry option in frontend

### Performance & UX

- [ ] T084 [P] Add loading states to all async operations on frontend
- [ ] T085 [P] Optimize API responses with appropriate status codes
- [ ] T086 [P] Add confirmation dialog for destructive actions (delete)

### Final Validation

- [ ] T087 Run quickstart.md verification checklist
- [ ] T088 [P] Test complete user journey: signup → signin → create → edit → toggle → delete → signout
- [ ] T089 [P] Verify all success criteria from spec.md are met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-9)**: All depend on Foundational phase completion
  - User stories can proceed in parallel after Phase 2
  - Or sequentially in priority order (US1 → US2 → US3 → US4 → US7 → US5 → US6)
- **Polish (Phase 10)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (Registration)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (Sign In)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (View Todos)**: Can start after Foundational (Phase 2) - Requires Sign In complete for full testing
- **User Story 4 (Create Todo)**: Can start after Foundational (Phase 2) - Requires View Todos for list display
- **User Story 5 (Edit Todo)**: Can start after Foundational (Phase 2) - Requires View Todos for context
- **User Story 6 (Delete Todo)**: Can start after Foundational (Phase 2) - Requires View Todos for context
- **User Story 7 (Toggle Completion)**: Can start after Foundational (Phase 2) - Requires View Todos for context

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before frontend integration
- Story complete before moving to polish

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, User Stories 1 and 2 can proceed in parallel
- Once Stories 1-2 complete, Stories 3-9 can proceed in parallel if team capacity allows
- Backend and frontend work for the same story can proceed in parallel

---

## Implementation Strategy

### MVP First (Minimal Viable Product)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Registration)
4. Complete Phase 4: User Story 2 (Sign In)
5. Complete Phase 5: User Story 3 (View Todos)
6. Complete Phase 6: User Story 4 (Create Todo)
7. **STOP and VALIDATE**: Test Stories 1-4 independently
8. Deploy/demo if ready (basic todo app with auth)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add Stories 1-2 (Auth) → Test independently → Deploy
3. Add Stories 3-4 (View + Create) → Test independently → Deploy (MVP!)
4. Add Story 7 (Toggle) → Test independently → Deploy
5. Add Stories 5-6 (Edit + Delete) → Test independently → Deploy
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Stories 1-2 (Auth backend + frontend)
   - Developer B: User Stories 3-4 (View + Create backend)
   - Developer C: User Stories 3-4 (View + Create frontend) or Stories 5-7
3. Stories complete and integrate independently

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1 | T001-T010 | Setup (10 tasks) |
| Phase 2 | T011-T030 | Foundational (20 tasks) |
| Phase 3 | T030-T036 | User Story 1: Registration (7 tasks) |
| Phase 4 | T037-T045 | User Story 2: Sign In (9 tasks) |
| Phase 5 | T046-T055 | User Story 3: View Todos (10 tasks) |
| Phase 6 | T056-T060 | User Story 4: Create Todo (5 tasks) |
| Phase 7 | T061-T066 | User Story 5: Edit Todo (6 tasks) |
| Phase 8 | T067-T072 | User Story 6: Delete Todo (6 tasks) |
| Phase 9 | T073-T077 | User Story 7: Toggle Completion (5 tasks) |
| Phase 10 | T078-T089 | Polish (12 tasks) |
| **Total** | **89 tasks** | Full Phase II implementation |

---

## Notes

- [P] tasks = different files, no dependencies - can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Verify tests fail before implementing (if tests included)
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
