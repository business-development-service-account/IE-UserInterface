"""
Tests for the ProjectService class.
"""

import pytest
from sqlalchemy.orm import Session

from app.services.project_service import ProjectService
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.utils.exceptions import (
    ProjectNotFoundException,
    ProjectAlreadyExistsException,
    DatabaseException
)


class TestProjectService:
    """Test cases for ProjectService."""

    def test_create_project_success(self, db_session: Session):
        """Test successful project creation."""
        service = ProjectService(db_session)
        project_data = ProjectCreate(name="Test Project", description="Test Description")

        result = service.create_project(project_data)

        assert result.id is not None
        assert result.name == "Test Project"
        assert result.description == "Test Description"
        assert result.is_active is True

    def test_create_project_duplicate_name(self, db_session: Session):
        """Test creating project with duplicate name raises exception."""
        service = ProjectService(db_session)
        project_data = ProjectCreate(name="Duplicate Project")

        # Create first project
        service.create_project(project_data)

        # Try to create duplicate
        with pytest.raises(ProjectAlreadyExistsException):
            service.create_project(project_data)

    def test_get_project_by_id_success(self, db_session: Session):
        """Test successful project retrieval by ID."""
        service = ProjectService(db_session)
        project_data = ProjectCreate(name="Test Project")
        created_project = service.create_project(project_data)

        retrieved_project = service.get_project_by_id(created_project.id)

        assert retrieved_project.id == created_project.id
        assert retrieved_project.name == "Test Project"

    def test_get_project_by_id_not_found(self, db_session: Session):
        """Test retrieving non-existent project raises exception."""
        service = ProjectService(db_session)

        with pytest.raises(ProjectNotFoundException):
            service.get_project_by_id(999)

    def test_get_all_projects_empty(self, db_session: Session):
        """Test retrieving all projects when none exist."""
        service = ProjectService(db_session)

        result = service.get_all_projects()
        assert result == []

    def test_get_all_projects_with_data(self, db_session: Session):
        """Test retrieving all projects when projects exist."""
        service = ProjectService(db_session)
        project_data1 = ProjectCreate(name="Project 1")
        project_data2 = ProjectCreate(name="Project 2")

        service.create_project(project_data1)
        service.create_project(project_data2)

        result = service.get_all_projects()
        assert len(result) == 2
        assert result[0].name == "Project 2"  # Should be ordered by created_at desc

    def test_update_project_success(self, db_session: Session):
        """Test successful project update."""
        service = ProjectService(db_session)
        project_data = ProjectCreate(name="Original Project", description="Original")
        created_project = service.create_project(project_data)

        update_data = ProjectUpdate(name="Updated Project", description="Updated")
        result = service.update_project(created_project.id, update_data)

        assert result.name == "Updated Project"
        assert result.description == "Updated"

    def test_update_project_not_found(self, db_session: Session):
        """Test updating non-existent project raises exception."""
        service = ProjectService(db_session)
        update_data = ProjectUpdate(name="Updated")

        with pytest.raises(ProjectNotFoundException):
            service.update_project(999, update_data)

    def test_update_project_duplicate_name(self, db_session: Session):
        """Test updating project with duplicate name raises exception."""
        service = ProjectService(db_session)
        project_data1 = ProjectCreate(name="Project 1")
        project_data2 = ProjectCreate(name="Project 2")

        created_project1 = service.create_project(project_data1)
        service.create_project(project_data2)

        update_data = ProjectUpdate(name="Project 2")
        with pytest.raises(ProjectAlreadyExistsException):
            service.update_project(created_project1.id, update_data)

    def test_delete_project_success(self, db_session: Session):
        """Test successful project deletion (soft delete)."""
        service = ProjectService(db_session)
        project_data = ProjectCreate(name="Test Project")
        created_project = service.create_project(project_data)

        service.delete_project(created_project.id)

        # Project should be marked as inactive
        with pytest.raises(ProjectNotFoundException):
            service.get_project_by_id(created_project.id)

    def test_delete_project_not_found(self, db_session: Session):
        """Test deleting non-existent project raises exception."""
        service = ProjectService(db_session)

        with pytest.raises(ProjectNotFoundException):
            service.delete_project(999)

    def test_get_project_count(self, db_session: Session):
        """Test getting project count."""
        service = ProjectService(db_session)

        # Initially should be 0
        assert service.get_project_count() == 0

        # Create some projects
        service.create_project(ProjectCreate(name="Project 1"))
        service.create_project(ProjectCreate(name="Project 2"))

        # Should be 2
        assert service.get_project_count() == 2

        # Delete one project
        projects = service.get_all_projects()
        service.delete_project(projects[0].id)

        # Should still be 2 because it's a soft delete
        assert service.get_project_count() == 1