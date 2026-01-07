# Implementation Plan: Phase II - Full-Stack Todo Application

**Branch**: `001-phase-2-todo-app` | **Date**: 2026-01-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-phase-2-todo-app/spec.md`

## Summary

Implement a full-stack todo application with user authentication, RESTful API backend, and responsive Next.js frontend. The application allows users to register, sign in, and manage their personal todo list with CRUD operations. All data persists in Neon Serverless PostgreSQL with user-level data isolation.

## Technical Context

**Language/Version**: Python 3.11+ (Backend), TypeScript (Frontend)
**Primary Dependencies**: FastAPI, SQLModel, Better Auth, Next.js 14+
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (Backend), Jest/Vitest (Frontend)
**Target Platform**: Web browser (desktop + mobile)
**Project Type**: Full-stack web application
**Performance Goals**: API response <200ms p95, 100 concurrent users
**Constraints**: No AI/agents, no background workers, no future phase features
**Scale/Scope**: Individual users with personal todo lists, ~100-1000 todos per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| I. Spec-Driven Development | Work follows Constitution → Specs → Plan → Tasks → Implement | ✅ PASS | This plan derived from approved spec |
| II. Agent Behavior Rules | No feature invention, no deviation from specs | ✅ PASS | Plan strictly follows Phase II specification |
| III. Phase Governance | Phase boundaries not crossed, features isolated | ✅ PASS | Only Phase II features included |
| IV. Technology Stack | Python REST API, Neon PostgreSQL, SQLModel, Next.js, Better Auth | ✅ PASS | All technologies from approved Phase II stack |
| V. Clean Architecture | Separation of concerns, dependency inversion | ✅ PASS | Layered architecture planned |
| VI. Testing and Quality | TDD, coverage requirements | ✅ PASS | Testing strategy defined in sections below |
| VII. Stateless Design | Session state externalized | ✅ PASS | Auth tokens, database persistence |

## Project Structure

### Documentation (this feature)

```text
specs/001-phase-2-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── auth.yaml        # Authentication API contracts
│   └── todos.yaml       # Todo API contracts
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/          # SQLModel entities (User, Todo)
│   ├── services/        # Business logic layer
│   ├── api/             # FastAPI routes and handlers
│   ├── schemas/         # Pydantic request/response models
│   └── core/            # Config, auth, database connection
├── tests/
│   ├── unit/            # Service and model tests
│   ├── integration/     # API endpoint tests
│   └── conftest.py      # Test fixtures
└── requirements.txt

frontend/
├── src/
│   ├── app/             # Next.js 14 App Router pages
│   │   ├── (auth)/      # Auth pages (signin, signup)
│   │   └── todos/       # Protected todo pages
│   ├── components/      # Reusable UI components
│   ├── lib/             # API client, auth utilities
│   └── styles/          # Global styles
├── tests/
│   └── e2e/             # End-to-end tests
└── package.json
```

**Structure Decision**: Web application (Option 2) with separate backend and frontend directories. Backend uses Python/FastAPI/SQLModel as per Phase II requirements. Frontend uses Next.js 14 with App Router. Tests organized by type (unit, integration, e2e).

---

## Backend Plan

### 1. REST API Framework (FastAPI)

FastAPI serves as the REST API framework for the following reasons:
- Native Python stack (matches Phase II requirements)
- Automatic OpenAPI documentation generation
- Built-in Pydantic validation
- ASGI async support for good performance
- Type-safe request/response handling

**Architecture Layers**:
- **api/**: HTTP handlers (routes, dependencies)
- **services/**: Business logic (auth service, todo service)
- **models/**: SQLModel database entities
- **schemas/**: Pydantic DTOs for API communication
- **core/**: Configuration, database session, auth context

### 2. API Routing Structure

All routes under `/api/` prefix with authentication handled by Better Auth middleware.

```
/api/auth/
  ├── POST /signup      # User registration
  ├── POST /signin      # User authentication
  ├── POST /signout     # End session
  └── GET /me           # Current user info

/api/todos/  (all require authentication)
  ├── GET /             # List user's todos
  ├── POST /            # Create new todo
  ├── GET /:id          # Get specific todo
  ├── PUT /:id          # Update todo
  ├── DELETE /:id       # Delete todo
  └── PATCH /:id/toggle # Toggle completion
```

### 3. Authentication Integration (Better Auth)

Better Auth provides authentication primitives:
- User signup/signin with email/password
- Session management via cookies
- Protected route middleware
- User model integration

**Auth Flow**:
1. User submits credentials to `/api/auth/signup` or `/api/auth/signin`
2. Server validates and creates session cookie
3. Subsequent requests include cookie for authentication
4. Protected endpoints verify session before processing

**Data Isolation**: All todo queries filter by `user_id` from authenticated session.

### 4. Data Persistence (Neon PostgreSQL + SQLModel)

SQLModel provides ORM capabilities with type safety:
- SQLModel entities map to PostgreSQL tables
- Async database sessions for request handling
- Connection pooling via Neon serverless driver

**Database Provider**: Neon Serverless PostgreSQL with async driver.

### 5. User-to-Todo Data Ownership

**Ownership Model**:
- User owns todos via foreign key relationship
- Todos.user_id references Users.id
- Cascade delete: deleting user removes all their todos

**Access Control**:
- All todo operations require authenticated session
- Todo queries automatically filter by `current_user.id`
- Attempting to access others' todos returns 403 Forbidden

### 6. Error Handling and Validation

**Validation Approach**:
- Pydantic models validate all request bodies
- SQLModel constraints validate database operations
- Custom error responses with user-friendly messages

**HTTP Status Codes**:
- 200: Success
- 201: Created (new resource)
- 400: Validation error
- 401: Unauthorized
- 403: Forbidden (not owner's resource)
- 404: Not found
- 500: Server error

**Error Response Format**:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "User-friendly message"
  }
}
```

---

## Frontend Plan

### 1. Next.js Application Structure

Next.js 14 with App Router provides:
- Server-side rendering for initial page loads
- Client-side interactivity for todo operations
- File-based routing for pages
- API routes for backend communication

**Directory Structure**:
```
src/app/
├── layout.tsx          # Root layout with auth provider
├── page.tsx            # Landing page (redirect based on auth)
├── (auth)/
│   ├── signin/
│   │   └── page.tsx   # Sign in page
│   └── signup/
│       └── page.tsx   # Sign up page
└── todos/
    ├── layout.tsx     # Protected routes wrapper
    ├── page.tsx       # Todo list dashboard
    └── [id]/
        └── page.tsx   # Individual todo view
```

### 2. Page-Level Routing

**Public Pages** (no auth required):
- `/` - Landing page, redirects to todos or signin
- `/signin` - Sign in form
- `/signup` - Sign up form

**Protected Pages** (auth required):
- `/todos` - Main todo list with CRUD operations
- `/todos/[id]` - Individual todo management

**Route Protection**: Middleware checks auth cookie, redirects to `/signin` if not authenticated.

### 3. Component Responsibilities

**UI Components** (src/components/):
- `Button.tsx` - Reusable button with variants
- `Input.tsx` - Form input with validation display
- `Card.tsx` - Container for todo items
- `TodoItem.tsx` - Individual todo display with actions
- `TodoList.tsx` - List container with empty state
- `Modal.tsx` - Confirmation dialogs

**Page Components**:
- Each page.tsx handles data fetching and renders UI components
- Server components for initial data load
- Client components for user interactions

### 4. API Communication Strategy

**API Client** (src/lib/api.ts):
- Centralized fetch wrapper for API calls
- Automatic cookie credential inclusion
- Error handling with user-friendly messages
- Type-safe response handling

**Key Functions**:
```typescript
api.get<T>(url: string): Promise<T>
api.post<T>(url: string, data: unknown): Promise<T>
api.put<T>(url: string, data: unknown): Promise<T>
api.delete<T>(url: string): Promise<T>
api.patch<T>(url: string, data: unknown): Promise<T>
```

### 5. Authentication State Handling

**Auth Context** (src/lib/auth.tsx):
- React context providing auth state to components
- Tracks: user, isAuthenticated, isLoading
- Provides: signin, signup, signout functions
- Persists: cookie-based (handled by browser)

**Auth Flow**:
1. App loads, checks auth cookie via `/api/auth/me`
2. Context updates with user state or redirects to signin
3. User interactions use context for auth-dependent actions

### 6. Responsive UI Strategy

**Mobile-First Approach**:
- Base styles target mobile screens
- Media queries for desktop enhancements
- Touch-friendly targets (minimum 44px)

**Responsive Breakpoints**:
- Mobile: < 640px (single column layout)
- Tablet: 640px - 1024px (adaptive padding)
- Desktop: > 1024px (full layout with sidebar potential)

**UI Framework**: Plain CSS with CSS Modules or Tailwind CSS (to be determined in tasks).

---

## Database Plan

### 1. User Data Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    todos: List["Todo"] = Relationship(back_populates="user")
```

**Constraints**:
- `email` must be unique, indexed for lookups
- `password_hash` stores bcrypt hash (not plain text)
- `created_at` uses UTC timestamp

### 2. Todo Data Model

```python
class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", on_delete="CASCADE")
    title: str = Field(max_length=200)
    is_complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: User = Relationship(back_populates="todos")
```

**Constraints**:
- `user_id` foreign key with CASCADE delete
- `title` limited to 200 characters
- `is_complete` defaults to false
- `updated_at` auto-updates on modification

### 3. User-Todo Relationship

**Relationship Type**: One-to-Many (User → Todos)

**Foreign Key**: `todos.user_id` → `users.id`

**Referential Integrity**:
- ON DELETE CASCADE: Deleting user removes all their todos
- No circular dependencies between entities

### 4. Migration Approach

**Schema Management**: Alembic for migration versioning

**Migration Strategy**:
1. Initial migration creates `users` and `todos` tables
2. Subsequent migrations handle schema changes
3. Down migrations available for rollback

**Development Flow**:
- Migrations run on application startup (development)
- Production deployments run migrations before starting

---

## Integration Plan

### 1. Frontend ↔ Backend Communication

**Protocol**: HTTP over REST API

**Data Format**: JSON for all requests and responses

**CORS Configuration**:
- Allow frontend origin (localhost for dev)
- Allow methods: GET, POST, PUT, PATCH, DELETE
- Allow headers: Content-Type, Authorization
- Allow credentials (cookies)

**Request Flow**:
1. Frontend sends request to backend API
2. Backend validates session from cookie
3. Backend processes request, returns JSON
4. Frontend updates UI based on response

### 2. Authentication Token/Session Flow

**Session Management**: Cookie-based (Better Auth)

**Cookie Properties**:
- `httpOnly`: true (not accessible via JavaScript)
- `secure`: true in production
- `sameSite`: "lax" for CSRF protection
- `maxAge`: 7 days (session duration)

**Auth Sequence**:
```
Signup:
  POST /api/auth/signup
  Body: { email, password }
  Response: 201, Set-Cookie (session)

Signin:
  POST /api/auth/signin
  Body: { email, password }
  Response: 200, Set-Cookie (session)

Authenticated Request:
  Request includes Cookie header
  Backend validates session, extracts user_id
  Process request with user context

Signout:
  POST /api/auth/signout
  Response: 200, Clear-Cookie
```

### 3. Local Development Setup

**Prerequisites**:
- Python 3.11+
- Node.js 18+
- PostgreSQL connection string (Neon)

**Backend Setup**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env  # Configure DATABASE_URL
alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend Setup**:
```bash
cd frontend
npm install
cp .env.example .env.local  # Configure API URL
npm run dev
```

**Access Points**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

No constitutional violations. Plan follows all principles.

---

## Testing Strategy

### Backend Testing

**Unit Tests** (pytest):
- Model validation tests
- Service logic tests
- Schema serialization tests

**Integration Tests** (pytest):
- API endpoint tests with test database
- Authentication flow tests
- Todo CRUD with user isolation

### Frontend Testing

**Unit Tests** (Jest/Vitest):
- Component rendering tests
- Auth context tests
- API client tests

**End-to-End Tests** (Playwright/Cypress):
- Signup → Signin → Create → Edit → Delete → Signout flow
- Responsive layout tests

---

## Follow-up Actions

1. **Create tasks.md** using `/sp.tasks` command
2. **Implement backend** following plan structure
3. **Implement frontend** following plan structure
4. **Run tests** to verify functionality
5. **Validate success criteria** from specification
