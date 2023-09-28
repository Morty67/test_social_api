from fastapi import HTTPException
from datetime import datetime

from app.repositories.like_repository import LikeRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository


class LikeService:
    def __init__(
        self,
        like_repo: LikeRepository,
        user_repo: UserRepository,
        post_repo: PostRepository,
    ):
        self.like_repo = like_repo
        self.user_repo = user_repo
        self.post_repo = post_repo

    async def add_like(self, user_id: int, post_id: int):
        user = await self.user_repo.get_user_by_id(user_id)
        post = await self.post_repo.get_post_by_id(post_id)

        if not user or not post:
            raise HTTPException(
                status_code=400, detail="There is no such post"
            )

        existing_like = await self.like_repo.get_like(user_id, post_id)

        if existing_like:
            raise HTTPException(
                status_code=400, detail="You have already liked this post"
            )

        like = await self.like_repo.create_like(user_id, post_id)
        # Update last request for user
        await self.user_repo.update_last_request(user)

        return like

    async def remove_like(self, user_id: int, post_id: int):
        existing_like = await self.like_repo.get_like(user_id, post_id)

        if existing_like:
            await self.like_repo.delete_like(user_id, post_id)

            # Update last request for user
            user = await self.user_repo.get_user_by_id(user_id)
            await self.user_repo.update_last_request(user)

            return True
        else:
            raise HTTPException(
                status_code=400, detail="You did not like this post"
            )

    async def get_likes_analytics(self, date_from: str, date_to: str):
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_to = datetime.strptime(date_to, "%Y-%m-%d")

        analytics = {}

        likes = await self.like_repo.get_likes_in_date_range(
            date_from, date_to
        )

        for like in likes:
            like_date = like.created_at.date()
            if like_date not in analytics:
                analytics[like_date] = {
                    "likes_count": 0,
                    "users_count": set(),
                    "likes_list": [],
                }

            analytics[like_date]["likes_count"] += 1
            analytics[like_date]["users_count"].add(like.user_id)
            analytics[like_date]["likes_list"].append(
                {
                    "user_id": like.user_id,
                    "post_id": like.post_id,
                    "is_liked": like.is_liked,
                    "id": like.id,
                    "created_at": like.created_at,
                }
            )

        for date, data in analytics.items():
            data["users_count"] = len(data["users_count"])
        if not analytics:
            return "There are currently no likes."
        return analytics
