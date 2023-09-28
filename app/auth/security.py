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
    return pwd_context.hash(password)


async def get_user(session: AsyncSession, username: str):
    result = await session.execute(
        select(User).filter(User.username == username)
    )
    return result.scalar_one_or_none()


async def get_current_profile(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
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
    return current_user


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str) -> str:
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
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
