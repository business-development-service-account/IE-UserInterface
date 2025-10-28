# Backend Software Architecture - Project Management System

## Overview
This document outlines the software architecture for a Python-based backend that provides project management functionality to the Next.js frontend. The initial implementation focuses on project creation capabilities with room for future expansion.

## Technology Stack
- **Runtime**: Python 3.11+
- **Web Framework**: FastAPI
- **Database**: SQLite (for development), with easy migration to PostgreSQL
- **ORM**: SQLAlchemy
- **Database Migrations**: Alembic
- **API Documentation**: OpenAPI/Swagger (built into FastAPI)
- **Validation**: Pydantic
- **Environment Management**: python-dotenv

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
│   └── alembic.ini
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Test configuration
│   ├── test_project_service.py
│   └── test_api_projects.py
├── .env.example               # Environment variables template
├── requirements.txt           # Python dependencies
└── run.py                    # Application runner
```

## Database Schema

### Project Table
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

## API Design

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints

#### Create Project
- **Endpoint**: `POST /projects`
- **Description**: Create a new project
- **Request Body**:
```json
{
    "name": "Project Name",
    "description": "Optional project description"
}
```
- **Response**:
```json
{
    "id": 1,
    "name": "Project Name",
    "description": "Optional project description",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "is_active": true
}
```
- **Error Responses**:
  - 400: Validation error
  - 409: Project name already exists

#### Get All Projects
- **Endpoint**: `GET /projects`
- **Description**: Retrieve all active projects
- **Response**:
```json
{
    "projects": [
        {
            "id": 1,
            "name": "Project Name",
            "description": "Optional project description",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "is_active": true
        }
    ],
    "count": 1
}
```

#### Get Project by ID
- **Endpoint**: `GET /projects/{project_id}`
- **Description**: Retrieve a specific project
- **Response**: Same as single project object above
- **Error Responses**:
  - 404: Project not found

#### Update Project
- **Endpoint**: `PUT /projects/{project_id}`
- **Description**: Update an existing project
- **Request Body**:
```json
{
    "name": "Updated Project Name",
    "description": "Updated description"
}
```
- **Response**: Updated project object
- **Error Responses**:
  - 400: Validation error
  - 404: Project not found
  - 409: Project name already exists

#### Delete Project
- **Endpoint**: `DELETE /projects/{project_id}`
- **Description**: Soft delete a project (set is_active to false)
- **Response**: 204 No Content
- **Error Responses**:
  - 404: Project not found

## Component Architecture

### Models Layer (`app/models/`)
- **Purpose**: Define database table structures using SQLAlchemy ORM
- **Key Components**:
  - `Project`: Main project entity with fields for name, description, timestamps
  - `BaseModel`: Common fields (id, created_at, updated_at) inherited by other models

### Schemas Layer (`app/schemas/`)
- **Purpose**: Define Pydantic models for request/response validation
- **Key Components**:
  - `ProjectCreate`: Schema for creating new projects
  - `ProjectUpdate`: Schema for updating existing projects
  - `ProjectResponse`: Schema for project responses
  - `ProjectList`: Schema for paginated project lists

### API Layer (`app/api/v1/endpoints/`)
- **Purpose**: Handle HTTP requests and responses
- **Key Components**:
  - FastAPI routers for different endpoints
  - Request validation using Pydantic schemas
  - Response formatting and error handling

### Services Layer (`app/services/`)
- **Purpose**: Implement business logic separate from API concerns
- **Key Components**:
  - `ProjectService`: Contains all project-related business operations
  - Database transaction management
  - Business rule validation

### Core Layer (`app/core/`)
- **Purpose**: Provide application-wide utilities and configuration
- **Key Components**:
  - Database connection and session management
  - Configuration settings from environment variables
  - Security utilities (prepared for future authentication)

## Error Handling Strategy

### Custom Exceptions
```python
class ProjectNotFoundException(Exception):
    pass

class ProjectAlreadyExistsException(Exception):
    pass

class ValidationException(Exception):
    pass
```

### Error Response Format
```json
{
    "error": {
        "code": "PROJECT_NOT_FOUND",
        "message": "Project with ID 123 not found",
        "details": {}
    }
}
```

## Configuration Management

### Environment Variables
```
# Database
DATABASE_URL=sqlite:///./app.db

# Application
APP_NAME="Project Management API"
APP_VERSION="1.0.0"
DEBUG=True

# Future: Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Development Setup

### Dependencies
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
alembic>=1.12.0
pydantic>=2.4.0
python-dotenv>=1.0.0
python-multipart>=0.0.6
```

### Database Initialization
1. Initialize Alembic: `alembic init alembic`
2. Create initial migration: `alembic revision --autogenerate -m "Initial migration"`
3. Apply migrations: `alembic upgrade head`

### Running the Application
```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode (future)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Future Extensibility

The architecture is designed to easily accommodate future requirements:

### Authentication & Authorization
- JWT-based authentication system
- User management with roles and permissions
- Project ownership and access control

### Advanced Features
- Project collections and categorization
- **File Manager system with folder hierarchy and inheritance**
- AI agent integration endpoints
- Real-time notifications with WebSockets
- Advanced search and filtering

### File Manager Implementation Plan

#### **Database Schema Additions**
```sql
-- Folders table for hierarchical file management
CREATE TABLE folders (
    id VARCHAR(36) PRIMARY KEY DEFAULT (hex(randomblob(16)),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    parent_folder_id VARCHAR(36), -- Self-referencing for hierarchy
    path TEXT NOT NULL,           -- Full path from root
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Junction table for folder-project associations
CREATE TABLE folder_project_access (
    id SERIAL PRIMARY KEY,
    folder_id VARCHAR(36) NOT NULL,
    project_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE(folder_id, project_id)
);
```

#### **API Endpoints to Add**
```python
# File Manager API (/api/v1/folders/)
POST /folders - Create folder
GET /folders - List all folders (with project access)
GET /folders/{folder_id} - Get folder details
PUT /folders/{folder_id} - Update folder
DELETE /folders/{folder_id} - Delete folder
POST /folders/{folder_id}/projects/{project_id} - Grant project access
DELETE /folders/{folder_id}/projects/{project_id} - Revoke project access
```

#### **Frontend Integration Status**
- ✅ File Manager navigation item added
- ✅ Folder creation and editing UI implemented
- ✅ Project access control UI implemented
- ✅ Folder hierarchy display with inheritance
- ❌ Backend integration needed (currently uses mock data)

#### **Key Features**
1. **Hierarchical Organization**: Folders can contain subfolders
2. **Inheritance System**: Subfolders inherit parent's project access
3. **Project Association**: Multiple projects can access same folder
4. **Path Management**: Automatic path generation for nested structures
5. **User Ownership**: Folder creation tracked by creating user

#### **Implementation Steps**
1. **Database Models**: Add Folder model and associations
2. **API Endpoints**: Implement CRUD operations for folders
3. **Service Layer**: Add folder business logic and inheritance logic
4. **Schemas**: Create Pydantic models for validation
5. **Frontend Integration**: Connect File Manager UI to real backend APIs
6. **Testing**: Add comprehensive tests for folder functionality

### Scalability
- Easy migration from SQLite to PostgreSQL
- Redis caching layer for frequently accessed data
- Background task processing with Celery
- API versioning strategy
- Rate limiting and monitoring

This architecture now provides complete file management capabilities while maintaining the clean, modular structure for easy maintenance and future enhancements.