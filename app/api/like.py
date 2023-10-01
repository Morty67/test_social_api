from fastapi import APIRouter, Depends, Query

from app.auth.security import get_current_active_profile
from app.models import User
from app.serializers.like_serializer import LikeAdd, LikeDelete
from app.services.like_service import LikeService
from app.utils.dependencies.services import get_like_service

router = APIRouter()


@router.post("/like_post/{post_id}", response_model=LikeAdd)
async def add_like(
    post_id: int,
    current_user: User = Depends(get_current_active_profile),
    service: LikeService = Depends(get_like_service),
):
    return await service.add_like(current_user.id, post_id)


@router.post("/delete_like_for_post/{post_id}", response_model=LikeDelete)
async def delete_like(
    post_id: int,
    current_user: User = Depends(get_current_active_profile),
    service: LikeService = Depends(get_like_service),
):
    removed = await service.remove_like(current_user.id, post_id)
    return LikeDelete(deleted=removed)


@router.get("/analytics/")
async def get_likes_analytics(
    date_from: str = Query(
        ..., description="Start date in the format YYYY-MM-DD"
    ),
    date_to: str = Query(
        ..., description="Completion date in the format YYYY-MM-DD"
    ),
    service: LikeService = Depends(get_like_service),
):
    return await service.get_likes_analytics(date_from, date_to)
