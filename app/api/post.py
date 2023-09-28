from fastapi import APIRouter, Depends

from app.auth.security import get_current_active_profile
from app.models import User
from app.serializers.post_serializer import PostResponse, PostCreate
from app.services.post_service import PostService
from app.utils.dependencies.services import get_post_service

router = APIRouter()


@router.post("/create_post/", response_model=PostResponse)
async def create_post(
    item: PostCreate,
    current_user: User = Depends(get_current_active_profile),
    service: PostService = Depends(get_post_service),
):
    return await service.create_post(item, current_user.id)
