# Frontend-Backend Integration Guide

This document outlines the specific steps and requirements to properly connect the Next.js frontend with the FastAPI backend for the LangGraph UserInterface project.

## 🎯 Integration Objectives

1. **Establish reliable communication** between frontend and backend
2. **Implement proper error handling** across the full stack
3. **Create consistent data models** between TypeScript and Python
4. **Set up development workflow** for seamless integration
5. **Implement authentication and security** measures

## 📋 Current Status Assessment

### ✅ Backend (READY)
- FastAPI server running on `http://localhost:8000`
- Project CRUD API endpoints implemented
- Database models and migrations complete
- API documentation available at `/docs`
- CORS middleware configured

### ❓ Frontend (NEEDS ASSESSMENT)
- Current frontend structure needs evaluation
- API client implementation required
- Type definitions need alignment
- Component integration needed

## 🔧 Integration Tasks

### Phase 1: Frontend Setup & API Client

#### 1.1 Environment Configuration
```bash
# Frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
```

#### 1.2 Install Required Dependencies
```bash
cd Frontend
npm install axios @tanstack/react-query
npm install --save-dev @types/node
```

#### 1.3 Create API Client Setup
**File**: `Frontend/src/lib/api.ts`
```typescript
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);
```

#### 1.4 Create API Service Functions
**File**: `Frontend/src/lib/projectService.ts`
```typescript
import { apiClient } from './api';

export interface Project {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface CreateProjectRequest {
  name: string;
  description?: string;
}

export interface UpdateProjectRequest {
  name?: string;
  description?: string;
}

export interface ProjectListResponse {
  projects: Project[];
  count: number;
}

export const projectService = {
  // Create project
  async createProject(data: CreateProjectRequest): Promise<Project> {
    const response = await apiClient.post('/api/v1/projects', data);
    return response.data;
  },

  // Get all projects
  async getProjects(): Promise<ProjectListResponse> {
    const response = await apiClient.get('/api/v1/projects');
    return response.data;
  },

  // Get project by ID
  async getProject(id: number): Promise<Project> {
    const response = await apiClient.get(`/api/v1/projects/${id}`);
    return response.data;
  },

  // Update project
  async updateProject(id: number, data: UpdateProjectRequest): Promise<Project> {
    const response = await apiClient.put(`/api/v1/projects/${id}`, data);
    return response.data;
  },

  // Delete project
  async deleteProject(id: number): Promise<void> {
    await apiClient.delete(`/api/v1/projects/${id}`);
  },
};
```

### Phase 2: React Components & State Management

#### 2.1 Create Project Components
**File**: `Frontend/src/components/ProjectCard.tsx`
```typescript
import React from 'react';
import { Project } from '@/lib/projectService';

interface ProjectCardProps {
  project: Project;
  onEdit?: (project: Project) => void;
  onDelete?: (id: number) => void;
}

export const ProjectCard: React.FC<ProjectCardProps> = ({
  project,
  onEdit,
  onDelete,
}) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-4">
      <h3 className="text-lg font-semibold text-gray-800 mb-2">
        {project.name}
      </h3>
      <p className="text-gray-600 mb-4">
        {project.description || 'No description available'}
      </p>
      <div className="flex justify-between items-center">
        <span className="text-sm text-gray-500">
          Created: {new Date(project.created_at).toLocaleDateString()}
        </span>
        <div className="space-x-2">
          {onEdit && (
            <button
              onClick={() => onEdit(project)}
              className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Edit
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(project.id)}
              className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Delete
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
```

#### 2.2 Create Project List Component
**File**: `Frontend/src/components/ProjectList.tsx`
```typescript
import React, { useState, useEffect } from 'react';
import { projectService, Project } from '@/lib/projectService';
import { ProjectCard } from './ProjectCard';

export const ProjectList: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      const response = await projectService.getProjects();
      setProjects(response.projects);
      setError(null);
    } catch (err) {
      setError('Failed to load projects');
      console.error('Error loading projects:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await projectService.deleteProject(id);
        setProjects(projects.filter(p => p.id !== id));
      } catch (err) {
        setError('Failed to delete project');
        console.error('Error deleting project:', err);
      }
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading projects...</div>;
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <div className="text-red-500 mb-4">{error}</div>
        <button
          onClick={loadProjects}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Retry
        </button>
      </div>
    );
  }

  if (projects.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No projects found. Create your first project to get started!
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        Projects ({projects.length})
      </h2>
      {projects.map((project) => (
        <ProjectCard
          key={project.id}
          project={project}
          onDelete={handleDelete}
        />
      ))}
    </div>
  );
};
```

#### 2.3 Create Project Form Component
**File**: `Frontend/src/components/ProjectForm.tsx`
```typescript
import React, { useState } from 'react';
import { projectService, CreateProjectRequest } from '@/lib/projectService';

interface ProjectFormProps {
  onSuccess?: () => void;
  onCancel?: () => void;
}

export const ProjectForm: React.FC<ProjectFormProps> = ({
  onSuccess,
  onCancel,
}) => {
  const [formData, setFormData] = useState<CreateProjectRequest>({
    name: '',
    description: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.name.trim()) {
      setError('Project name is required');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await projectService.createProject(formData);
      setFormData({ name: '', description: '' });
      onSuccess?.();
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to create project');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Create New Project
      </h2>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="name" className="block text-gray-700 font-medium mb-2">
            Project Name *
          </label>
          <input
            type="text"
            id="name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter project name"
            required
          />
        </div>

        <div className="mb-6">
          <label htmlFor="description" className="block text-gray-700 font-medium mb-2">
            Description
          </label>
          <textarea
            id="description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={4}
            placeholder="Enter project description (optional)"
          />
        </div>

        <div className="flex space-x-4">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 disabled:bg-blue-300 disabled:cursor-not-allowed"
          >
            {loading ? 'Creating...' : 'Create Project'}
          </button>
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="flex-1 bg-gray-500 text-white py-2 px-4 rounded-md hover:bg-gray-600"
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};
```

### Phase 3: Page Implementation

#### 3.1 Create Main Dashboard Page
**File**: `Frontend/src/app/page.tsx`
```typescript
'use client';

import React, { useState } from 'react';
import { ProjectList } from '@/components/ProjectList';
import { ProjectForm } from '@/components/ProjectForm';

export default function Home() {
  const [showForm, setShowForm] = useState(false);

  const handleProjectCreated = () => {
    setShowForm(false);
    // ProjectList will automatically refresh when it re-renders
    window.location.reload();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            LangGraph Project Manager
          </h1>
          <p className="text-gray-600">
            Manage your LangGraph agents and workflows
          </p>
        </header>

        <main>
          <div className="mb-8">
            <button
              onClick={() => setShowForm(!showForm)}
              className="bg-green-500 text-white px-6 py-2 rounded-md hover:bg-green-600"
            >
              {showForm ? 'Cancel' : 'Create New Project'}
            </button>
          </div>

          {showForm && (
            <div className="mb-8">
              <ProjectForm
                onSuccess={handleProjectCreated}
                onCancel={() => setShowForm(false)}
              />
            </div>
          )}

          <ProjectList />
        </main>
      </div>
    </div>
  );
}
```

### Phase 4: Error Handling & Loading States

#### 4.1 Create Error Boundary Component
**File**: `Frontend/src/components/ErrorBoundary.tsx`
```typescript
import React from 'react';

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends React.Component<
  React.PropsWithChildren<{}>,
  ErrorBoundaryState
> {
  constructor(props: React.PropsWithChildren<{}>) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="bg-white rounded-lg shadow-md p-8 max-w-md">
            <h2 className="text-2xl font-bold text-red-600 mb-4">
              Something went wrong
            </h2>
            <p className="text-gray-600 mb-4">
              {this.state.error?.message || 'An unexpected error occurred'}
            </p>
            <button
              onClick={() => window.location.reload()}
              className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
```

#### 4.2 Update Layout with Error Boundary
**File**: `Frontend/src/app/layout.tsx`
```typescript
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { ErrorBoundary } from '@/components/ErrorBoundary';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'LangGraph Project Manager',
  description: 'Manage your LangGraph agents and workflows',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ErrorBoundary>
          {children}
        </ErrorBoundary>
      </body>
    </html>
  );
}
```

### Phase 5: Development Workflow

#### 5.1 Setup Development Scripts
**File**: `Frontend/package.json` (add to scripts section)
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "dev:full": "concurrently \"npm run dev\" \"cd ../Backend && python run.py\""
  }
}
```

#### 5.2 Integration Testing
**File**: `Frontend/src/__tests__/integration.test.tsx`
```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { ProjectList } from '@/components/ProjectList';
import { projectService } from '@/lib/projectService';

// Mock the API service
jest.mock('@/lib/projectService');

describe('Project Integration', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should load and display projects', async () => {
    const mockProjects = [
      {
        id: 1,
        name: 'Test Project',
        description: 'A test project',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
        is_active: true,
      },
    ];

    (projectService.getProjects as jest.Mock).mockResolvedValue({
      projects: mockProjects,
      count: 1,
    });

    render(<ProjectList />);

    await waitFor(() => {
      expect(screen.getByText('Test Project')).toBeInTheDocument();
    });
  });
});
```

## 🔧 Configuration Checklist

### Backend Configuration
- [x] CORS middleware configured to allow frontend origin
- [x] Database migrations applied
- [x] API endpoints tested and working
- [x] Error handling implemented

### Frontend Configuration
- [ ] Environment variables set
- [ ] API client implemented
- [ ] TypeScript types aligned with backend schemas
- [ ] Error handling implemented
- [ ] Loading states added
- [ ] Components tested

### Integration Testing
- [ ] Frontend can successfully call backend API
- [ ] Error responses handled properly
- [ ] Data types match between frontend and backend
- [ ] Network errors handled gracefully

## 🚀 Deployment Considerations

### Environment Variables
```bash
# Production Frontend (.env.local)
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NEXT_PUBLIC_API_VERSION=v1

# Production Backend (.env)
DATABASE_URL=postgresql://user:pass@host:port/db
DEBUG=False
SECRET_KEY=your-production-secret
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### CORS Configuration
Update backend CORS settings for production:
```python
# Backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## 📋 Testing Strategy

### Unit Tests
- Component testing with React Testing Library
- API service testing with mocked responses
- Utility function testing

### Integration Tests
- Full API call testing
- Error scenario testing
- Loading state testing

### E2E Tests (Future)
- Playwright or Cypress for full user flows
- Cross-browser testing
- Mobile responsiveness testing

## 🔄 Next Steps

1. **Immediate**: Implement the basic frontend components and API integration
2. **Short-term**: Add comprehensive error handling and loading states
3. **Medium-term**: Implement authentication and authorization
4. **Long-term**: Add advanced features like file uploads, real-time updates

## 🐛 Common Issues & Solutions

### CORS Errors
- Ensure backend CORS allows frontend origin
- Check API URLs in frontend environment variables

### Type Mismatches
- Keep TypeScript interfaces in sync with backend Pydantic models
- Use shared type definitions when possible

### Network Errors
- Implement retry logic for failed requests
- Add user-friendly error messages
- Handle offline scenarios

---

This integration guide provides a complete roadmap for connecting the frontend and backend components of the LangGraph UserInterface project.