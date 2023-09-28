from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.security import get_current_active_profile
from app.auth.token_serializer import Token
from app.models import User
from app.serializers.user_serializer import (
    UserCreate,
    UserResponse,
    UserActivityResponse,
)
from app.services.user_service import UserService
from app.utils.dependencies.services import get_user_service

router = APIRouter()


@router.post("/create_user/", response_model=UserResponse)
async def create_profile(
    item: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.register_user(item)


@router.post("/login/", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
):
    access_token = await service.login_user(
        form_data.username, form_data.password
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_active_profile),
):
    return current_user


@router.get("/user/activity/", response_model=UserActivityResponse)
async def get_user_activity(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    return UserActivityResponse(
        last_login=await user_service.get_last_login(user_id),
        last_request=await user_service.get_last_request(user_id),
    )
