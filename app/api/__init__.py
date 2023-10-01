from fastapi import APIRouter

from app.api.user import router as user_router
from app.api.post import router as post_router
from app.api.like import router as like_router


api_router = APIRouter()

api_router.include_router(
    post_router, prefix="/posts", tags=["Post"]
)
api_router.include_router(user_router, prefix="/users", tags=["User"])
api_router.include_router(
    like_router, prefix="/likes", tags=["Like"]
)
