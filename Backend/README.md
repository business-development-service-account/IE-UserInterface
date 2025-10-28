# Project Management API Backend

A FastAPI-based backend for managing projects with SQLAlchemy ORM and Alembic migrations.

## Features

- **Project CRUD Operations**: Create, read, update, and delete projects
- **RESTful API**: Well-designed API with proper HTTP status codes and error handling
- **Database Support**: SQLite for development, easy migration to PostgreSQL
- **Data Validation**: Pydantic schemas for request/response validation
- **Database Migrations**: Alembic for database schema management
- **Comprehensive Testing**: Unit and integration tests with pytest
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## Quick Start

### 1. Installation

```bash
# Clone the repository and navigate to the backend directory
cd /path/to/Backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
# Copy the environment template
cp .env.example .env

# Edit .env with your configuration (default values work for development)
```

### 3. Database Setup

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 4. Run the Application

```bash
# Using the convenient runner script
python run.py

# Or directly with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Endpoints

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/projects` | Create a new project |
| GET | `/api/v1/projects` | Get all active projects |
| GET | `/api/v1/projects/{id}` | Get a specific project |
| PUT | `/api/v1/projects/{id}` | Update a project |
| DELETE | `/api/v1/projects/{id}` | Soft delete a project |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |

## Project Structure

```
Backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration settings
│   │   ├── database.py        # Database connection and session management
│   │   └── security.py        # Security utilities (future implementation)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── project.py         # Project database model
│   │   └── base.py            # Base model with common fields
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── project.py         # Pydantic models for request/response
│   │   └── base.py            # Base schemas with common fields
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py            # Dependencies (database sessions, etc.)
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── projects.py # Project-related endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── project_service.py # Business logic for project operations
│   └── utils/
│       ├── __init__.py
│       └── exceptions.py      # Custom exceptions
├── alembic/                   # Database migrations
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Test configuration
│   ├── test_project_service.py
│   └── test_api_projects.py
├── .env.example               # Environment variables template
├── requirements.txt           # Python dependencies
├── run.py                    # Application runner
├── alembic.ini              # Alembic configuration
└── README.md                 # This file
```

## Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api_projects.py

# Run tests with verbose output
pytest -v
```

## Database Migrations

### Creating New Migrations

```bash
# Create a new migration after changing models
alembic revision --autogenerate -m "Description of changes"

# Apply the migration
alembic upgrade head
```

### Migration Commands

```bash
# Show current revision
alembic current

# Show migration history
alembic history

# Revert to previous migration
alembic downgrade -1

# Revert to specific migration
alembic downgrade <revision_hash>
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./app.db` | Database connection URL |
| `APP_NAME` | `Project Management API` | Application name |
| `APP_VERSION` | `1.0.0` | Application version |
| `DEBUG` | `True` | Debug mode |
| `SECRET_KEY` | `None` | JWT secret key (future) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration (future) |

## Error Handling

The API provides consistent error responses in the following format:

```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message",
        "details": {}
    }
}
```

Common error codes:
- `PROJECT_NOT_FOUND` (404): Project with given ID not found
- `PROJECT_ALREADY_EXISTS` (409): Project name already exists
- `DATABASE_ERROR` (500): Database operation failed
- `VALIDATION_ERROR` (422): Request validation failed

## Development

### Code Style

The project follows Python best practices:
- Type hints are used throughout
- Pydantic for data validation
- SQLAlchemy for database operations
- Clear separation of concerns (API, Services, Models)

### Adding New Features

1. **Models**: Define database models in `app/models/`
2. **Schemas**: Create Pydantic schemas in `app/schemas/`
3. **Services**: Implement business logic in `app/services/`
4. **Endpoints**: Add API endpoints in `app/api/v1/endpoints/`
5. **Tests**: Write tests in `tests/`
6. **Migrations**: Create and apply database migrations

## Future Enhancements

The architecture is designed to easily accommodate:

- **Authentication & Authorization**: JWT-based system with user management
- **Advanced Features**: File uploads, real-time notifications, search/filtering
- **Scalability**: PostgreSQL migration, Redis caching, background tasks
- **Monitoring**: Rate limiting, logging, metrics

## License

This project is part of the LangGraph UserInterface system.