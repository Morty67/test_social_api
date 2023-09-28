from fastapi import HTTPException

from app.models import Post
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.serializers.post_serializer import PostCreate, PostResponse


class PostService:
    def __init__(self, post_repo: PostRepository, user_repo: UserRepository):
        self.post_repo = post_repo
        self.user_repo = user_repo

    async def create_post(self, post_data: PostCreate, user_id: int):
        user = await self.post_repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        post_data_dict = post_data.dict()
        post_data_dict["user_id"] = user_id
        new_post = Post(**post_data_dict)
        await self.post_repo.save(new_post)

        await self.user_repo.update_last_request(user)

        return PostResponse(
            id=new_post.id,
            title=new_post.title,
            content=new_post.content,
            author=user.username,
        )
