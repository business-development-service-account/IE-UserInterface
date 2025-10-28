from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Import from the existing app
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.core.database import get_db
from auth_implementation.services.user_service import UserService
from auth_implementation.models.user import User
from auth_implementation.core.security import verify_token

# OAuth2 scheme for JWT authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Get user service instance."""
    return UserService(db)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"error": {"code": "INVALID_CREDENTIALS", "message": "Could not validate credentials"}},
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify token and get user ID
    user_id = verify_token(token, token_type="access")
    if user_id is None:
        raise credentials_exception

    try:
        user_id = int(user_id)
    except ValueError:
        raise credentials_exception

    # Get user from database
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "INACTIVE_USER", "message": "Inactive user"}}
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "UNVERIFIED_USER", "message": "Email not verified"}}
        )

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "INACTIVE_USER", "message": "Inactive user"}}
        )
    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Get current verified user."""
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "UNVERIFIED_USER", "message": "Email not verified"}}
        )
    return current_user


async def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> Optional[User]:
    """Get current user if token is provided, otherwise return None."""
    if not token:
        return None

    try:
        return await get_current_user(token, user_service)
    except HTTPException:
        return None


def get_user_from_refresh_token(
    refresh_token: str,
    user_service: UserService = Depends(get_user_service)
) -> User:
    """Get user from refresh token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"error": {"code": "INVALID_REFRESH_TOKEN", "message": "Invalid refresh token"}},
    )

    # Verify refresh token
    user_id = verify_token(refresh_token, token_type="refresh")
    if user_id is None:
        raise credentials_exception

    try:
        user_id = int(user_id)
    except ValueError:
        raise credentials_exception

    # Get user from database
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "INACTIVE_USER", "message": "Inactive user"}}
        )

    # Verify session exists and is valid
    session = user_service.get_valid_session(user_id, refresh_token)
    if not session:
        raise credentials_exception

    return user