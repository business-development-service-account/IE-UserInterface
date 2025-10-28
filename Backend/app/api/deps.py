from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.project_service import ProjectService


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """Dependency to get ProjectService instance."""
    return ProjectService(db)