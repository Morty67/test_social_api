from pydantic import BaseModel
from datetime import datetime


class PostCreate(BaseModel):
    title: str
    content: str
    created_at: datetime = datetime.utcnow()


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str

    class Config:
        orm_mode = True
