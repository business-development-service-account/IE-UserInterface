from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseResponse


class ProjectBase(BaseModel):
    """Base project schema with common fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Name of the project")
    description: Optional[str] = Field(None, description="Optional project description")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Project name cannot be empty')
        return v.strip()


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""

    pass


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project."""

    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Updated name of the project")
    description: Optional[str] = Field(None, description="Updated project description")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Project name cannot be empty')
        return v.strip() if v else v


class ProjectResponse(BaseResponse, ProjectBase):
    """Schema for project responses."""

    pass


class ProjectList(BaseModel):
    """Schema for paginated project list responses."""

    projects: List[ProjectResponse] = Field(..., description="List of projects")
    count: int = Field(..., description="Total number of projects")

    class Config:
        from_attributes = True