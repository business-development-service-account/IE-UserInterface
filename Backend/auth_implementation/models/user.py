from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Import from the existing app for now
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.models.base import BaseModel


class User(BaseModel):
    """User model for authentication and user management."""

    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships will be added when we integrate with existing models
    # owned_projects = relationship("Project", back_populates="owner")
    # project_memberships = relationship("ProjectMember", back_populates="user")
    # audit_logs = relationship("AuditLog", back_populates="user")
    # sessions = relationship("UserSession", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    @property
    def is_authenticated(self):
        """Check if user is authenticated."""
        return self.is_active and self.is_verified