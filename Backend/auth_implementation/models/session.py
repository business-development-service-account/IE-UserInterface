from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Import from the existing app for now
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.models.base import BaseModel


class UserSession(BaseModel):
    """User session model for JWT token management."""

    __tablename__ = "user_sessions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_hash = Column(String(255), nullable=False, unique=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships will be added when we integrate
    # user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id}, active={self.is_active})>"

    @property
    def is_expired(self):
        """Check if session is expired."""
        return func.now() > self.expires_at

    @property
    def is_valid(self):
        """Check if session is both active and not expired."""
        return self.is_active and not self.is_expired