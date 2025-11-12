"""Authentication and authorization utilities"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.user import User
from config.database import get_db
from config.settings import settings
from lib.exceptions import AuthenticationError

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer token scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError as e:
        raise AuthenticationError(f"Invalid token: {str(e)}")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get the current authenticated user from JWT token"""
    token = credentials.credentials

    try:
        payload = decode_token(token)
        user_id = payload.get("sub")

        if not user_id or not isinstance(user_id, str):
            raise AuthenticationError("Invalid token payload")

    except JWTError:
        raise AuthenticationError("Could not validate credentials")

    # Get user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise AuthenticationError("User not found")

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get the current active user (can add active status check here)"""
    return current_user


# Optional: Dependency for optional authentication
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """Get current user if authenticated, None otherwise"""
    if not credentials:
        return None

    try:
        return await get_current_user(credentials, db)
    except AuthenticationError:
        return None
