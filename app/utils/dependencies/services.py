from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.like_repository import LikeRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.services.like_service import LikeService
from app.services.post_service import PostService
from app.services.user_service import UserService
from app.utils.dependencies.get_session import get_session


def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    repo = UserRepository(session)
    service = UserService(user_repo=repo)

    return service


def get_post_service(
    session: AsyncSession = Depends(get_session),
) -> PostService:
    repo = PostRepository(session)
    user_repo = UserRepository(session)
    service = PostService(post_repo=repo, user_repo=user_repo)
    return service


def get_like_service(
    session: AsyncSession = Depends(get_session),
) -> LikeService:
    repo = LikeRepository(session)
    post_repo = PostRepository(session)
    user_repo = UserRepository(session)
    service = LikeService(
        like_repo=repo, post_repo=post_repo, user_repo=user_repo
    )
    return service
