from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime


# Base schemas
class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool = True


class UserCreate(BaseModel):
    """User registration schema."""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if len(v) > 50:
            raise ValueError('Username must be less than 50 characters')
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain alphanumeric characters, underscores, and hyphens')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(BaseModel):
    """User profile update schema."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInDBBase(UserBase):
    """User schema as stored in database."""
    id: int
    is_verified: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDBBase):
    """User response schema."""
    pass


class UserInDB(UserInDBBase):
    """User schema with hashed password."""
    hashed_password: str


# Authentication schemas
class Token(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token data schema."""
    username: Optional[str] = None
    user_id: Optional[int] = None


class LoginRequest(BaseModel):
    """Login request schema."""
    username_or_email: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class PasswordChange(BaseModel):
    """Password change schema."""
    current_password: str
    new_password: str

    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class PasswordReset(BaseModel):
    """Password reset request schema."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema."""
    token: str
    new_password: str

    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class EmailVerification(BaseModel):
    """Email verification schema."""
    token: str