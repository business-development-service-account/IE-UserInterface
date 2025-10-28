from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

# Import from the existing app
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.core.database import get_db
from auth_implementation.services.user_service import UserService
from auth_implementation.schemas.user import (
    User, UserCreate, UserUpdate, LoginRequest, Token,
    RefreshTokenRequest, PasswordChange, PasswordReset, PasswordResetConfirm
)
from auth_implementation.api_deps.auth import (
    get_user_service, get_current_verified_user, get_user_from_refresh_token
)
from auth_implementation.core.security import (
    create_access_token, create_refresh_token, verify_password,
    generate_password_reset_token, verify_password_reset_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Register a new user."""
    try:
        user = user_service.create_user(user_create)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": "REGISTRATION_FAILED", "message": "Registration failed"}}
        )


@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    request: Request,
    user_service: UserService = Depends(get_user_service)
):
    """Authenticate user and return tokens."""
    user = user_service.authenticate_user(login_data.username_or_email, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"code": "INVALID_CREDENTIALS", "message": "Incorrect username or password"}},
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "EMAIL_NOT_VERIFIED", "message": "Please verify your email before logging in"}}
        )

    # Create access and refresh tokens
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(subject=user.id)

    # Create session
    user_service.create_user_session(user.id, access_token, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
    }


@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_data: RefreshTokenRequest,
    user_service: UserService = Depends(get_user_service)
):
    """Refresh access token using refresh token."""
    try:
        user = get_user_from_refresh_token(refresh_data.refresh_token, user_service)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"code": "INVALID_REFRESH_TOKEN", "message": "Invalid refresh token"}}
        )

    # Create new tokens
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token(subject=user.id)

    # Revoke old refresh token and create new session
    user_service.revoke_session(user.id, refresh_data.refresh_token)
    user_service.create_user_session(user.id, access_token, new_refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/logout")
def logout(
    refresh_data: RefreshTokenRequest,
    current_user: User = Depends(get_current_verified_user),
    user_service: UserService = Depends(get_user_service)
):
    """Logout user and revoke refresh token."""
    success = user_service.revoke_session(current_user.id, refresh_data.refresh_token)

    if success:
        return {"message": "Successfully logged out"}
    else:
        return {"message": "Logout completed (session was already expired)"}


@router.post("/logout-all")
def logout_all(
    current_user: User = Depends(get_current_verified_user),
    user_service: UserService = Depends(get_user_service)
):
    """Logout user from all devices."""
    revoked_count = user_service.revoke_all_sessions(current_user.id)

    return {
        "message": f"Successfully logged out from {revoked_count} devices"
    }


@router.get("/me", response_model=User)
def get_current_user_info(
    current_user: User = Depends(get_current_verified_user)
):
    """Get current user information."""
    return current_user


@router.put("/me", response_model=User)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_verified_user),
    user_service: UserService = Depends(get_user_service)
):
    """Update current user profile."""
    try:
        updated_user = user_service.update_user(current_user.id, user_update)
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": "UPDATE_FAILED", "message": "Failed to update user profile"}}
        )


@router.post("/change-password")
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_verified_user),
    user_service: UserService = Depends(get_user_service)
):
    """Change user password."""
    try:
        user_service.change_password(
            current_user.id,
            password_data.current_password,
            password_data.new_password
        )
        # Revoke all sessions to force re-login on all devices
        user_service.revoke_all_sessions(current_user.id)

        return {"message": "Password changed successfully. Please login again."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"code": "PASSWORD_CHANGE_FAILED", "message": "Failed to change password"}}
        )


@router.post("/forgot-password")
def forgot_password(
    password_data: PasswordReset,
    request: Request,
    user_service: UserService = Depends(get_user_service)
):
    """Request password reset."""
    user = user_service.get_user_by_email(password_data.email)

    if not user:
        # Don't reveal that user doesn't exist
        return {"message": "If an account with this email exists, a password reset link has been sent."}

    # Generate password reset token
    reset_token = generate_password_reset_token(user.email)

    # TODO: Send email with reset token
    # For now, just return the token (in production, this should be sent via email)
    # For development purposes only:
    if os.getenv("DEBUG", "false").lower() == "true":
        return {
            "message": "Password reset token generated (development mode)",
            "reset_token": reset_token
        }

    return {"message": "If an account with this email exists, a password reset link has been sent."}


@router.post("/reset-password")
def reset_password(
    password_data: PasswordResetConfirm,
    user_service: UserService = Depends(get_user_service)
):
    """Reset password with token."""
    email = verify_password_reset_token(password_data.token)

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "INVALID_TOKEN", "message": "Invalid or expired token"}}
        )

    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "USER_NOT_FOUND", "message": "User not found"}}
        )

    # Change password
    from auth_implementation.core.security import get_password_hash
    user.hashed_password = get_password_hash(password_data.new_password)

    # Revoke all sessions to force re-login
    user_service.revoke_all_sessions(user.id)

    user_service.db.commit()

    return {"message": "Password reset successfully. Please login with your new password."}


@router.get("/verify-email/{token}")
def verify_email(
    token: str,
    user_service: UserService = Depends(get_user_service)
):
    """Verify user email."""
    email = verify_password_reset_token(token)

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "INVALID_TOKEN", "message": "Invalid or expired verification token"}}
        )

    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "USER_NOT_FOUND", "message": "User not found"}}
        )

    if user.is_verified:
        return {"message": "Email already verified"}

    user_service.verify_user(user.id)

    return {"message": "Email verified successfully. You can now login."}


@router.get("/sessions")
def get_active_sessions(
    current_user: User = Depends(get_current_verified_user),
    user_service: UserService = Depends(get_user_service)
):
    """Get active sessions for current user."""
    # This would require extending the UserSession model to include device info
    # For now, return a basic response
    return {
        "message": "Active sessions feature coming soon",
        "user_id": current_user.id
    }