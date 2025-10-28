from sqlalchemy import Column, String, Text
from app.models.base import BaseModel


class Project(BaseModel):
    """Project model for storing project information."""

    __tablename__ = "projects"

    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"