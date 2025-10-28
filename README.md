# LangGraph UserInterface

A fully integrated full-stack web application for managing LangGraph agents and workflows with a modern React frontend and FastAPI backend.

## 🎯 Current Status: **✅ Integration Complete**

The frontend-backend integration is fully functional and ready for use. Both services are running and connected with working project management features.

## 🏗️ Architecture Overview

This project consists of two fully integrated components:

- **Frontend**: Next.js 15 React application with TypeScript and Tailwind CSS
- **Backend**: FastAPI Python application with SQLAlchemy ORM and SQLite database

Both components work together seamlessly with real-time project management capabilities.

## 📁 Project Structure

```
LangGraph/UserInterface/
├── Frontend/                    # Next.js React application
│   ├── src/
│   │   ├── app/                # App Router pages
│   │   ├── components/         # Reusable React components
│   │   ├── lib/               # Utility functions and configurations
│   │   └── types/             # TypeScript type definitions
│   ├── public/                # Static assets
│   ├── package.json           # Node.js dependencies
│   └── README.md              # Frontend-specific documentation
├── Backend/                     # FastAPI Python application
│   ├── app/
│   │   ├── api/               # API endpoints and routing
│   │   ├── core/              # Core configurations (database, security)
│   │   ├── models/            # SQLAlchemy database models
│   │   ├── schemas/           # Pydantic data validation schemas
│   │   ├── services/          # Business logic layer
│   │   └── utils/             # Utility functions and exceptions
│   ├── alembic/               # Database migrations
│   ├── tests/                 # Test suite
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Backend-specific documentation
└── README.md                  # This file - project overview
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18+ recommended)
- **Python 3.11+**
- **Git**

### 1. Clone the Repository

```bash
git clone <repository-url>
cd LangGraph/UserInterface
```

### 2. Backend Setup

```bash
cd Backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Environment setup
cp .env.example .env

# Database setup
alembic upgrade head

# Start the backend server
python run.py
```

The backend will be available at: http://localhost:8000

### 3. Frontend Setup

```bash
cd ../Frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at: http://localhost:3000

### 4. Access the Application

🌐 **Live Application**: http://localhost:3002/projects

- **Frontend Application**: http://localhost:3002/projects
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

> ✅ **Both services are currently running and fully integrated!**

## 🌐 Frontend Features

### Technology Stack
- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand for global state
- **HTTP Client**: Axios with interceptors
- **Development**: ESLint, Prettier, TypeScript

### ✅ **Implemented Features**
- **Project Dashboard**: Complete overview of all projects
- **Project Management**: Full CRUD operations (Create, Read, Update, Delete)
- **Real-time Updates**: Projects appear immediately after creation
- **Responsive Design**: Mobile-first approach
- **Type Safety**: Full TypeScript implementation
- **Modern UI**: Clean, intuitive interface with modal forms
- **Error Handling**: User-friendly error messages and validation
- **Loading States**: Smooth loading indicators
- **Navigation**: Sidebar navigation with Projects, Collections, Settings

### 🔜 **Placeholder Features (Coming Soon)**
- **Chat Interface**: Ready for LangGraph agent integration
- **Skills Editor**: Ready for skill template management
- **File Management**: Ready for document uploads and management
- **Tool Selection**: Ready for agent tool configuration

### Development Commands
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # TypeScript type checking
```

## 🔧 Backend Features

### Technology Stack
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: SQLite (development), PostgreSQL ready (production)
- **ORM**: SQLAlchemy 2.0+
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Testing**: pytest with coverage

### ✅ **Implemented API Endpoints**

#### Projects
- `POST /api/v1/projects` - ✅ Create new project
- `GET /api/v1/projects` - ✅ List all active projects
- `GET /api/v1/projects/{id}` - ✅ Get specific project
- `PUT /api/v1/projects/{id}` - ✅ Update project
- `DELETE /api/v1/projects/{id}` - ✅ Soft delete project

#### System
- `GET /` - ✅ API information and links
- `GET /health` - ✅ Health check endpoint

### 🔧 **Advanced Features**
- **Error Handling**: Structured error responses with proper HTTP status codes
- **CORS Support**: Configured for frontend integration
- **Auto-documentation**: OpenAPI/Swagger documentation at `/docs`
- **Database Migrations**: Alembic for schema management
- **Type Safety**: Pydantic models for request/response validation

### Development Commands
```bash
source venv/bin/activate  # Activate virtual environment

# Development
python run.py             # Start development server
uvicorn app.main:app --reload --port 8000  # Alternative start method

# Database
alembic revision --autogenerate -m "Description"  # Create migration
alembic upgrade head     # Apply migrations
alembic downgrade -1     # Rollback one migration

# Testing
pytest                   # Run all tests
pytest --cov=app        # Run tests with coverage
pytest -v               # Verbose test output
```

## 🔄 Frontend-Backend Integration

### API Communication

The frontend communicates with the backend through RESTful API calls:

```typescript
// Example API call from frontend
const response = await fetch('http://localhost:8000/api/v1/projects', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'New Project',
    description: 'Project description'
  })
});

const project = await response.json();
```

### ✅ **Working Data Flow**

1. **Frontend** makes HTTP requests to **Backend API** ✅
2. **Backend** validates requests using Pydantic schemas ✅
3. **Backend** processes business logic in service layer ✅
4. **Backend** interacts with database via SQLAlchemy ORM ✅
5. **Backend** returns JSON responses to **Frontend** ✅
6. **Frontend** updates UI based on API responses ✅

### ✅ **Error Handling Implementation**

- **Backend**: Structured error responses with proper HTTP status codes ✅
- **Frontend**: Error boundaries and user-friendly error messages ✅
- **Network**: Proper handling of connectivity issues ✅
- **Validation**: Client-side and server-side form validation ✅

### 🔄 **Integration Status**

The frontend and backend are fully integrated with:
- **CORS Configuration**: Properly configured for cross-origin requests
- **Type Safety**: Matching TypeScript and Python types
- **Real-time Updates**: Projects appear immediately in UI
- **Error Handling**: Comprehensive error reporting
- **State Management**: Zustand store synchronized with API responses

## 🧪 Testing

### Frontend Testing
```bash
cd Frontend
npm test                # Run Jest tests
npm run test:coverage   # Run tests with coverage
```

### Backend Testing
```bash
cd Backend
source venv/bin/activate
pytest                 # Run all tests
pytest --cov=app      # Run tests with coverage
pytest tests/test_project_service.py  # Run specific test file
```

## 🚀 Deployment

### Production Backend Setup

1. **Environment Variables**:
   ```env
   DATABASE_URL=postgresql://user:password@localhost/dbname
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ```

2. **Database Migration**:
   ```bash
   alembic upgrade head
   ```

3. **Production Server**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### Production Frontend Setup

1. **Build Application**:
   ```bash
   cd Frontend
   npm run build
   ```

2. **Start Production Server**:
   ```bash
   npm run start
   ```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
# Database
DATABASE_URL=sqlite:///./app.db

# Application
APP_NAME="Project Management API"
APP_VERSION="1.0.0"
DEBUG=True

# Security (future implementation)
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📋 Development Workflow

### 1. Feature Development
1. Create feature branch from main
2. Implement backend changes (models, API, tests)
3. Implement frontend changes (components, pages, tests)
4. Run tests for both frontend and backend
5. Test integration between frontend and backend
6. Submit pull request

### 2. Code Quality
- **TypeScript**: Strict type checking enabled
- **ESLint**: Code linting and formatting
- **Prettier**: Code formatting
- **pytest**: Backend testing with coverage
- **Testing**: Comprehensive test coverage

### 3. Database Changes
1. Modify SQLAlchemy models in `Backend/app/models/`
2. Generate migration: `alembic revision --autogenerate -m "Description"`
3. Apply migration: `alembic upgrade head`
4. Update frontend types if needed

## 🐛 Troubleshooting

### Common Issues

#### Backend
- **Port already in use**: Change port in run.py or kill existing process
- **Database errors**: Run `alembic upgrade head` to ensure migrations are applied
- **Import errors**: Ensure virtual environment is activated

#### Frontend
- **Module not found**: Run `npm install` to ensure dependencies are installed
- **TypeScript errors**: Check types in `types/` directory
- **Build errors**: Clear `.next` folder and rebuild

#### Integration
- **CORS errors**: Backend CORS middleware should allow frontend origin
- **Connection refused**: Ensure both servers are running on correct ports
- **API errors**: Check backend logs for detailed error information

### Getting Help

1. Check individual README files:
   - `/Frontend/README.md` for frontend-specific information
   - `/Backend/README.md` for backend-specific information

2. Review API documentation at http://localhost:8000/docs

3. Check console output and logs for detailed error messages

## 🛣️ Roadmap

### ✅ **Completed Features**
- **Frontend-Backend Integration**: Full CRUD operations working
- **Project Management**: Create, read, update, delete projects
- **Real-time UI Updates**: Projects appear immediately
- **Error Handling**: Comprehensive error reporting
- **Type Safety**: End-to-end TypeScript integration
- **Database Schema**: Projects with proper relationships
- **API Documentation**: Auto-generated OpenAPI docs

### 🔜 **In Progress / Planned Features**
- **Authentication & Authorization**: User management with JWT
- **LangGraph Agent Integration**: Chat interface for agent interaction
- **Skill Template Management**: Create and manage agent skills
- **File Management**: Document uploads and project files
- **Tool Selection**: Configure agent tools and capabilities
- **Advanced Project Features**: File uploads, sharing, collaboration
- **Real-time Updates**: WebSocket integration for live updates
- **Enhanced UI**: More sophisticated components and interactions

### 🔧 **Technical Improvements**
- **Database**: PostgreSQL migration for production scalability
- **Caching**: Redis integration for performance
- **Background Tasks**: Celery for async operations
- **Testing**: E2E testing with Playwright
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Monitoring**: Logging, metrics, error tracking

## 📄 License

This project is part of the LangGraph ecosystem and follows its licensing terms.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request with a clear description

---

**Last Updated**: October 27, 2024
**Version**: 1.0.0
**Status**: ✅ **Integration Complete - Live and Functional**

### 🎯 **Current Status**
- ✅ Backend API running on http://localhost:8000
- ✅ Frontend running on http://localhost:3002
- ✅ Full CRUD operations working
- ✅ Real-time project management
- ✅ Type-safe integration
- ✅ Comprehensive error handling
- ✅ Production-ready architecture

### 🚀 **Quick Access**
- **Application**: http://localhost:3002/projects
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

**Ready for development and testing!** 🎉