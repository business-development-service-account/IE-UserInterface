from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status

# Import from the existing app
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.core.database import get_db
from auth_implementation.models.user import User
from auth_implementation.models.session import UserSession
from auth_implementation.schemas.user import UserCreate, UserUpdate
from auth_implementation.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    generate_token_hash,
    verify_token
)


class UserService:
    """Service for user management and authentication."""

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email_or_username(self, email_or_username: str) -> Optional[User]:
        """Get user by email or username."""
        return self.db.query(User).filter(
            or_(User.email == email_or_username, User.username == email_or_username)
        ).first()

    def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""
        # Check if user already exists
        if self.get_user_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": {"code": "EMAIL_ALREADY_EXISTS", "message": "Email already registered"}}
            )

        if self.get_user_by_username(user_create.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": {"code": "USERNAME_ALREADY_EXISTS", "message": "Username already taken"}}
            )

        # Create new user
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password,
            full_name=user_create.full_name,
            is_active=True,
            is_verified=False  # Should be verified via email
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def authenticate_user(self, username_or_email: str, password: str) -> Optional[User]:
        """Authenticate user with username/email and password."""
        user = self.get_user_by_email_or_username(username_or_username)

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        # Update last login
        user.last_login = datetime.utcnow()
        self.db.commit()

        return user

    def update_user(self, user_id: int, user_update: UserUpdate) -> User:
        """Update user profile."""
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": {"code": "USER_NOT_FOUND", "message": "User not found"}}
            )

        # Check if email is being updated and if it's already taken
        if user_update.email and user_update.email != user.email:
            if self.get_user_by_email(user_update.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"error": {"code": "EMAIL_ALREADY_EXISTS", "message": "Email already registered"}}
                )
            user.email = user_update.email
            user.is_verified = False  # Re-verification required for new email

        if user_update.full_name is not None:
            user.full_name = user_update.full_name

        self.db.commit()
        self.db.refresh(user)

        return user

    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """Change user password."""
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": {"code": "USER_NOT_FOUND", "message": "User not found"}}
            )

        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": {"code": "INVALID_CURRENT_PASSWORD", "message": "Current password is incorrect"}}
            )

        user.hashed_password = get_password_hash(new_password)
        self.db.commit()

        return True

    def create_user_session(self, user_id: int, access_token: str, refresh_token: str) -> UserSession:
        """Create a new user session."""
        # Calculate expiration times
        access_expires_at = datetime.utcnow() + timedelta(minutes=15)  # Access token expires in 15 minutes
        refresh_expires_at = datetime.utcnow() + timedelta(days=7)   # Refresh token expires in 7 days

        # Hash the refresh token for storage (access token is not stored)
        refresh_token_hash = generate_token_hash(refresh_token)

        # Create session
        session = UserSession(
            user_id=user_id,
            token_hash=refresh_token_hash,
            expires_at=refresh_expires_at,
            is_active=True
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def get_valid_session(self, user_id: int, refresh_token: str) -> Optional[UserSession]:
        """Get valid user session."""
        refresh_token_hash = generate_token_hash(refresh_token)

        session = self.db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.token_hash == refresh_token_hash,
            UserSession.is_active == True
        ).first()

        if not session:
            return None

        # Check if session is expired
        if datetime.utcnow() > session.expires_at:
            session.is_active = False
            self.db.commit()
            return None

        return session

    def revoke_session(self, user_id: int, refresh_token: str) -> bool:
        """Revoke a user session."""
        refresh_token_hash = generate_token_hash(refresh_token)

        session = self.db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.token_hash == refresh_token_hash,
            UserSession.is_active == True
        ).first()

        if session:
            session.is_active = False
            self.db.commit()
            return True

        return False

    def revoke_all_sessions(self, user_id: int) -> int:
        """Revoke all sessions for a user."""
        sessions = self.db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True
        ).all()

        for session in sessions:
            session.is_active = False

        self.db.commit()
        return len(sessions)

    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions."""
        expired_sessions = self.db.query(UserSession).filter(
            UserSession.expires_at < datetime.utcnow(),
            UserSession.is_active == True
        ).all()

        for session in expired_sessions:
            session.is_active = False

        self.db.commit()
        return len(expired_sessions)

    def verify_user(self, user_id: int) -> bool:
        """Verify user email."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        user.is_verified = True
        self.db.commit()
        return True

    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate user account."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        user.is_active = False
        # Revoke all sessions
        self.revoke_all_sessions(user_id)
        self.db.commit()
        return True

    def activate_user(self, user_id: int) -> bool:
        """Activate user account."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        user.is_active = True
        self.db.commit()
        return True