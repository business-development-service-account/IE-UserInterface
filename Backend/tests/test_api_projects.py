"""
Tests for the projects API endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestProjectsAPI:
    """Test cases for projects API endpoints."""

    def test_create_project_success(self, client: TestClient, sample_project_data):
        """Test successful project creation via API."""
        response = client.post("/api/v1/projects", json=sample_project_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_project_data["name"]
        assert data["description"] == sample_project_data["description"]
        assert data["id"] is not None
        assert data["is_active"] is True

    def test_create_project_duplicate_name(self, client: TestClient, sample_project_data):
        """Test creating project with duplicate name via API."""
        # Create first project
        client.post("/api/v1/projects", json=sample_project_data)

        # Try to create duplicate
        response = client.post("/api/v1/projects", json=sample_project_data)

        assert response.status_code == 409
        error = response.json()
        assert error["error"]["code"] == "PROJECT_ALREADY_EXISTS"

    def test_create_project_validation_error(self, client: TestClient):
        """Test creating project with invalid data via API."""
        invalid_data = {"name": "", "description": "Valid description"}

        response = client.post("/api/v1/projects", json=invalid_data)

        assert response.status_code == 422  # Validation error

    def test_get_all_projects_empty(self, client: TestClient):
        """Test retrieving all projects when none exist via API."""
        response = client.get("/api/v1/projects")

        assert response.status_code == 200
        data = response.json()
        assert data["projects"] == []
        assert data["count"] == 0

    def test_get_all_projects_with_data(self, client: TestClient, sample_project_data):
        """Test retrieving all projects when projects exist via API."""
        # Create some projects
        client.post("/api/v1/projects", json=sample_project_data)
        client.post("/api/v1/projects", json={"name": "Another Project"})

        response = client.get("/api/v1/projects")

        assert response.status_code == 200
        data = response.json()
        assert len(data["projects"]) == 2
        assert data["count"] == 2

    def test_get_project_by_id_success(self, client: TestClient, sample_project_data):
        """Test retrieving project by ID via API."""
        # Create a project
        create_response = client.post("/api/v1/projects", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Get the project
        response = client.get(f"/api/v1/projects/{project_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == project_id
        assert data["name"] == sample_project_data["name"]

    def test_get_project_by_id_not_found(self, client: TestClient):
        """Test retrieving non-existent project via API."""
        response = client.get("/api/v1/projects/999")

        assert response.status_code == 404
        error = response.json()
        assert error["error"]["code"] == "PROJECT_NOT_FOUND"

    def test_update_project_success(self, client: TestClient, sample_project_data):
        """Test updating project via API."""
        # Create a project
        create_response = client.post("/api/v1/projects", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Update the project
        update_data = {"name": "Updated Project", "description": "Updated description"}
        response = client.put(f"/api/v1/projects/{project_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Project"
        assert data["description"] == "Updated description"

    def test_update_project_not_found(self, client: TestClient, sample_project_update_data):
        """Test updating non-existent project via API."""
        response = client.put("/api/v1/projects/999", json=sample_project_update_data)

        assert response.status_code == 404
        error = response.json()
        assert error["error"]["code"] == "PROJECT_NOT_FOUND"

    def test_update_project_duplicate_name(self, client: TestClient, sample_project_data):
        """Test updating project with duplicate name via API."""
        # Create two projects
        client.post("/api/v1/projects", json={"name": "Project 1"})
        create_response = client.post("/api/v1/projects", json={"name": "Project 2"})
        project_id = create_response.json()["id"]

        # Try to update Project 2 with Project 1's name
        response = client.put(f"/api/v1/projects/{project_id}", json={"name": "Project 1"})

        assert response.status_code == 409
        error = response.json()
        assert error["error"]["code"] == "PROJECT_ALREADY_EXISTS"

    def test_delete_project_success(self, client: TestClient, sample_project_data):
        """Test deleting project via API."""
        # Create a project
        create_response = client.post("/api/v1/projects", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Delete the project
        response = client.delete(f"/api/v1/projects/{project_id}")

        assert response.status_code == 204

        # Verify project is deleted
        get_response = client.get(f"/api/v1/projects/{project_id}")
        assert get_response.status_code == 404

    def test_delete_project_not_found(self, client: TestClient):
        """Test deleting non-existent project via API."""
        response = client.delete("/api/v1/projects/999")

        assert response.status_code == 404
        error = response.json()
        assert error["error"]["code"] == "PROJECT_NOT_FOUND"

    def test_root_endpoint(self, client: TestClient):
        """Test the root endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert "redoc" in data

    def test_health_check(self, client: TestClient):
        """Test the health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "app_name" in data
        assert "version" in data