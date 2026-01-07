# Evolution of Todo - Phase II

Full-stack todo application with user authentication, built as Phase II of the "Evolution of Todo" project.

## Features

- **User Registration** - Create a new account with email and password
- **User Sign In** - Authenticate and access personal todo list
- **View Todos** - Display all todos belonging to the authenticated user
- **Create Todo** - Add new todos to personal list
- **Edit Todo** - Update existing todo titles
- **Delete Todo** - Remove todos from the list
- **Toggle Completion** - Mark todos as complete/incomplete

## Tech Stack

### Backend
- Python 3.11+
- FastAPI (REST API)
- SQLModel (ORM)
- Neon Serverless PostgreSQL
- Alembic (Database migrations)
- Better Auth (Authentication)

### Frontend
- Next.js 14 (App Router)
- TypeScript
- CSS (Custom styles)

## Project Structure

```
phase1/
├── backend/
│   ├── src/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Config, database, auth
│   │   ├── models/       # SQLModel entities
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   ├── alembic/          # Database migrations
│   ├── tests/            # Unit and integration tests
│   ├── requirements.txt
│   └── pyproject.toml
│
└── frontend/
    ├── src/
    │   ├── app/          # Next.js pages
    │   ├── components/   # Reusable UI components
    │   ├── lib/          # API client, auth context
    │   └── styles/       # Global styles
    ├── package.json
    └── tsconfig.json
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL connection string (Neon)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL

# Run migrations
alembic upgrade head

# Start the server
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# No changes needed for local development

# Start development server
npm run dev
```

The app will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/signin` - Sign in
- `POST /api/auth/signout` - Sign out
- `GET /api/auth/me` - Get current user

### Todos
- `GET /api/todos` - List user's todos
- `POST /api/todos` - Create todo
- `GET /api/todos/:id` - Get specific todo
- `PUT /api/todos/:id` - Update todo
- `DELETE /api/todos/:id` - Delete todo
- `PATCH /api/todos/:id/toggle` - Toggle completion

## User Stories Implemented

| Story | Description | Status |
|-------|-------------|--------|
| US1 | User Registration | Complete |
| US2 | User Sign In | Complete |
| US3 | View Todos | Complete |
| US4 | Create Todo | Complete |
| US5 | Edit Todo | Complete |
| US6 | Delete Todo | Complete |
| US7 | Toggle Completion | Complete |

## Success Criteria

- [x] Users can register and sign in within 60 seconds
- [x] Users can create and view todos within 2 seconds
- [x] Authenticated users can only access their own todos
- [x] Data persists across sessions
- [x] Responsive UI for desktop and mobile

## License

MIT
