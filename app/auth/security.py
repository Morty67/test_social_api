from typing import Annotated
from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession


from app.auth.token_serializer import TokenData
from app.models import User
from app.utils.dependencies.get_session import get_session
from config import (
    pwd_context,
    oauth2_scheme,
    ALGORITHM,
    SECRET_KEY,
)


def get_password_hash(password):
    """
    Hashes the input password using the application's password hashing algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


async def get_user(session: AsyncSession, username: str):
    """
    Retrieves a user from the database by their username.

    Args:
        session (AsyncSession): The asynchronous database session.
        username (str): The username of the user to retrieve.

    Returns:
        User: The user model instance.

    Raises:
        HTTPException: If the user with the specified username does not exist.
    """
    result = await session.execute(
        select(User).filter(User.username == username)
    )
    return result.scalar_one_or_none()


async def get_current_profile(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    """
    Retrieves the current user's profile based on the provided JWT token.

    Args:
        token (str, optional): The JWT token obtained from the request headers.
        session (AsyncSession, optional): The asynchronous database session.

    Returns:
        User: The user model instance representing the current user's profile.

    Raises:
        HTTPException: If the token is invalid or does not correspond to any user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    profile = await get_user(session, username=token_data.username)
    if profile is None:
        raise credentials_exception
    return profile


async def get_current_active_profile(
    current_user: Annotated[User, Depends(get_current_profile)]
):
    """
    Ensures the current user is active by returning the user model instance.

    Args:
        current_user (User): The user model instance obtained from the current request.

    Returns:
        User: The active user model instance.
    """
    return current_user


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies the provided plain password against the stored hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str) -> str:
    """
    Authenticates a user based on their username and password and returns a JWT access token.

    Args:
        username (str): The username of the user trying to authenticate.
        password (str): The password provided by the user.

    Returns:
        str: The JWT access token if authentication is successful.

    Raises:
        HTTPException: If the provided username or password is incorrect.
    """
    profile = await get_user(username)
    if not profile or not await verify_password(
        password, profile.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_jwt_token(data={"sub": profile.username})
    return access_token


async def create_jwt_token(data: dict, expires_minutes: int = 30) -> str:
    """
    Creates a JWT token with the provided data and expiration time.

    Args:
        data (dict): The payload data to be encoded into the token.
        expires_minutes (int, optional): The token expiration time in minutes. Defaults to 30 minutes.

    Returns:
        str: The encoded JWT token.
    """
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
