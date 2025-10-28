from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets

# Import from the existing app
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes or 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.

    Args:
        subject: Token subject (usually user ID or email)
        expires_delta: Custom expiration time

    Returns:
        JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key or secrets.token_urlsafe(32), algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT refresh token.

    Args:
        subject: Token subject (usually user ID or email)
        expires_delta: Custom expiration time

    Returns:
        JWT refresh token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key or secrets.token_urlsafe(32), algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token to verify
        token_type: Expected token type ("access" or "refresh")

    Returns:
        Token subject if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, settings.secret_key or secrets.token_urlsafe(32), algorithms=[ALGORITHM])
        subject: str = payload.get("sub")
        token_type_in_token: str = payload.get("type")

        if subject is None or token_type_in_token != token_type:
            return None

        return subject
    except JWTError:
        return None


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def generate_password_reset_token(email: str) -> str:
    """
    Generate a password reset token.

    Args:
        email: User email

    Returns:
        Password reset token
    """
    delta = timedelta(hours=1)  # Reset token expires in 1 hour
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email, "type": "password_reset"},
        settings.secret_key or secrets.token_urlsafe(32),
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verify a password reset token.

    Args:
        token: Password reset token

    Returns:
        User email if valid, None otherwise
    """
    try:
        decoded_token = jwt.decode(token, settings.secret_key or secrets.token_urlsafe(32), algorithms=[ALGORITHM])
        return decoded_token["sub"]
    except JWTError:
        return None


def generate_token_hash(token: str) -> str:
    """
    Generate a hash for storing tokens in database.

    Args:
        token: JWT token

    Returns:
        SHA256 hash of the token
    """
    import hashlib
    return hashlib.sha256(token.encode()).hexdigest()


def generate_secure_random_string(length: int = 32) -> str:
    """
    Generate a cryptographically secure random string.

    Args:
        length: Length of the random string

    Returns:
        Secure random string
    """
    return secrets.token_urlsafe(length)