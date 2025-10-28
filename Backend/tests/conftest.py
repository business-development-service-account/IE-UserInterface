"""
Pytest configuration and fixtures for the Project Management API tests.
"""

import pytest
import tempfile
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db, Base
from app.core.config import settings


# Test database configuration
@pytest.fixture(scope="session")
def test_db():
    """Create a temporary database for testing."""
    # Create a temporary SQLite database
    db_fd, db_path = tempfile.mkstemp()
    test_database_url = f"sqlite:///{db_path}"

    # Create test engine
    engine = create_engine(
        test_database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    yield TestingSessionLocal

    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def db_session(test_db):
    """Create a database session for testing."""
    session = test_db()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """Create a test client for the FastAPI application."""
    # Override the database dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Clean up overrides
    app.dependency_overrides.clear()


@pytest.fixture
def sample_project_data():
    """Sample project data for testing."""
    return {
        "name": "Test Project",
        "description": "A test project for testing purposes"
    }


@pytest.fixture
def sample_project_update_data():
    """Sample project update data for testing."""
    return {
        "name": "Updated Test Project",
        "description": "Updated test project description"
    }