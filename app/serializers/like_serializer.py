from pydantic import BaseModel
from datetime import datetime


class LikeAction(BaseModel):
    is_liked: bool


class LikeAdd(LikeAction):
    post_id: int
    id: int
    user_id: int
    created_at: datetime


class LikeDelete(BaseModel):
    deleted: bool
