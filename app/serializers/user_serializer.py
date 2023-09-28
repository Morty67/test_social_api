from typing import Optional

from pydantic import BaseModel, EmailStr

import datetime


class UserCreate(BaseModel):
    username: str
    full_name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: EmailStr
    created_at: Optional[datetime.datetime] = None
    last_login: Optional[datetime.datetime] = None
    last_request: Optional[datetime.datetime] = None


class UserActivityResponse(BaseModel):
    last_login: datetime
    last_request: datetime

    class Config:
        arbitrary_types_allowed = True
