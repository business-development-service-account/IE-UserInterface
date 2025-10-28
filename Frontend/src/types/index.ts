// Backend-aligned Project interface
export interface Project {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

// User interface
export interface User {
  id: number;
  name: string;
  email: string;
  avatar?: string;
  created_at: string;
}

// File Manager interfaces
export interface Folder {
  id: string;
  name: string;
  description?: string;
  parentFolderId?: string;
  projectIds: number[]; // Projects that have access to this folder
  created_at: string;
  updated_at: string;
  createdBy: number; // User ID
  path: string; // Full path from root
  isExpanded: boolean; // For UI state
}

export interface CreateFolderRequest {
  name: string;
  description?: string;
  parentFolderId?: string;
  projectIds: number[];
}

// Project Group for UI grouping functionality
export interface ProjectGroup {
  id: string;
  name: string;
  projects: Project[];
  isCollapsed: boolean;
  created_at: string;
}

// Legacy interface for future features (messages, skills, files)
export interface ProjectWithFeatures extends Project {
  messages: Message[];
  skills: SkillTemplate[];
  files: UploadedFile[];
  enabledTools: string[];
}

export interface SkillTemplate {
  id: string;
  name: string;
  description: string;
  content: string;
}

export interface Collection {
  id: string;
  name: string;
  description: string;
}

export interface Message {
  id: string;
  content: string;
  timestamp: Date;
  type: 'user' | 'assistant';
}

export interface UploadedFile {
  id: string;
  name: string;
  size: number;
  type: string;
  uploadedAt: Date;
}

export interface Settings {
  availableTools: string[];
  basicValues: Record<string, any>;
}

// API request/response types matching backend
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

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

// Error response type from backend
export interface ApiError {
  error: {
    code: string;
    message: string;
    details: Record<string, any>;
  };
}