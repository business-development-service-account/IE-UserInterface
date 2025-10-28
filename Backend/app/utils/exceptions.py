"""Custom exceptions for the Project Management API."""


class ProjectNotFoundException(Exception):
    """Raised when a project is not found."""

    def __init__(self, project_id: int):
        self.project_id = project_id
        super().__init__(f"Project with ID {project_id} not found")


class ProjectAlreadyExistsException(Exception):
    """Raised when attempting to create a project that already exists."""

    def __init__(self, project_name: str):
        self.project_name = project_name
        super().__init__(f"Project with name '{project_name}' already exists")


class ValidationException(Exception):
    """Raised when validation fails."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Validation error: {message}")


class DatabaseException(Exception):
    """Raised when a database operation fails."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Database error: {message}")