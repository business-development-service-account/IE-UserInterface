from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.utils.exceptions import (
    ProjectNotFoundException,
    ProjectAlreadyExistsException,
    DatabaseException
)


class ProjectService:
    """Service class for project-related business logic."""

    def __init__(self, db: Session):
        self.db = db

    def create_project(self, project_data: ProjectCreate) -> Project:
        """Create a new project."""
        try:
            # Check if project with the same name already exists
            existing_project = self.db.query(Project).filter(
                Project.name == project_data.name,
                Project.is_active == True
            ).first()

            if existing_project:
                raise ProjectAlreadyExistsException(project_data.name)

            db_project = Project(**project_data.dict())
            self.db.add(db_project)
            self.db.commit()
            self.db.refresh(db_project)
            return db_project

        except IntegrityError as e:
            self.db.rollback()
            raise ProjectAlreadyExistsException(project_data.name)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(f"Failed to create project: {str(e)}")

    def get_project_by_id(self, project_id: int) -> Project:
        """Retrieve a project by its ID."""
        try:
            project = self.db.query(Project).filter(
                Project.id == project_id,
                Project.is_active == True
            ).first()

            if not project:
                raise ProjectNotFoundException(project_id)

            return project

        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to retrieve project: {str(e)}")

    def get_all_projects(self) -> List[Project]:
        """Retrieve all active projects."""
        try:
            projects = self.db.query(Project).filter(
                Project.is_active == True
            ).order_by(Project.created_at.desc()).all()
            return projects

        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to retrieve projects: {str(e)}")

    def update_project(self, project_id: int, project_data: ProjectUpdate) -> Project:
        """Update an existing project."""
        try:
            project = self.get_project_by_id(project_id)

            # If updating name, check for conflicts
            if project_data.name and project_data.name != project.name:
                existing_project = self.db.query(Project).filter(
                    Project.name == project_data.name,
                    Project.is_active == True,
                    Project.id != project_id
                ).first()

                if existing_project:
                    raise ProjectAlreadyExistsException(project_data.name)

            # Update only provided fields
            update_data = project_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(project, field, value)

            self.db.commit()
            self.db.refresh(project)
            return project

        except IntegrityError as e:
            self.db.rollback()
            raise ProjectAlreadyExistsException(project_data.name)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(f"Failed to update project: {str(e)}")

    def delete_project(self, project_id: int) -> None:
        """Soft delete a project (set is_active to False)."""
        try:
            project = self.get_project_by_id(project_id)
            project.is_active = False
            self.db.commit()

        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseException(f"Failed to delete project: {str(e)}")

    def get_project_count(self) -> int:
        """Get the total count of active projects."""
        try:
            count = self.db.query(Project).filter(
                Project.is_active == True
            ).count()
            return count

        except SQLAlchemyError as e:
            raise DatabaseException(f"Failed to get project count: {str(e)}")