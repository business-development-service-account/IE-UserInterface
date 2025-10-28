from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.api.deps import get_project_service
from app.services.project_service import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectList
from app.utils.exceptions import (
    ProjectNotFoundException,
    ProjectAlreadyExistsException,
    DatabaseException
)

router = APIRouter()


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    project_service: ProjectService = Depends(get_project_service)
):
    """Create a new project."""
    try:
        return project_service.create_project(project_data)
    except ProjectAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": {
                    "code": "PROJECT_ALREADY_EXISTS",
                    "message": str(e),
                    "details": {}
                }
            }
        )
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": str(e),
                    "details": {}
                }
            }
        )


@router.get("/projects", response_model=ProjectList)
def get_all_projects(project_service: ProjectService = Depends(get_project_service)):
    """Retrieve all active projects."""
    try:
        projects = project_service.get_all_projects()
        count = project_service.get_project_count()
        return ProjectList(projects=projects, count=count)
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": str(e),
                    "details": {}
                }
            }
        )


@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service)
):
    """Retrieve a specific project by ID."""
    try:
        return project_service.get_project_by_id(project_id)
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "PROJECT_NOT_FOUND",
                    "message": str(e),
                    "details": {}
                }
            }
        )
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": str(e),
                    "details": {}
                }
            }
        )


@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    project_service: ProjectService = Depends(get_project_service)
):
    """Update an existing project."""
    try:
        return project_service.update_project(project_id, project_data)
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "PROJECT_NOT_FOUND",
                    "message": str(e),
                    "details": {}
                }
            }
        )
    except ProjectAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": {
                    "code": "PROJECT_ALREADY_EXISTS",
                    "message": str(e),
                    "details": {}
                }
            }
        )
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": str(e),
                    "details": {}
                }
            }
        )


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service)
):
    """Soft delete a project (set is_active to false)."""
    try:
        project_service.delete_project(project_id)
    except ProjectNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "PROJECT_NOT_FOUND",
                    "message": str(e),
                    "details": {}
                }
            }
        )
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": str(e),
                    "details": {}
                }
            }
        )