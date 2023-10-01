from fastapi import HTTPException
from datetime import datetime

from app.repositories.like_repository import LikeRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository


class LikeService:
    """
    Service class for handling like-related operations including adding, removing, and analytics.

    This class provides methods to add and remove likes on posts, as well as retrieving analytics
    for likes within a specified date range.

    Attributes:
        like_repo (LikeRepository): An instance of LikeRepository for database operations related to likes.
        user_repo (UserRepository): An instance of UserRepository for user-related database operations.
        post_repo (PostRepository): An instance of PostRepository for post-related database operations.
    """

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
        """
        Adds a like to a post for the specified user.

        Args:
            user_id (int): The ID of the user adding the like.
            post_id (int): The ID of the post to be liked.

        Returns:
            dict: A dictionary containing like details if successful.

        Raises:
            HTTPException: If the user or post does not exist.
        """
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
        """
        Removes a like from a post for the specified user.

        Args:
            user_id (int): The ID of the user removing the like.
            post_id (int): The ID of the post to be unliked.

        Returns:
            bool: True if the like is successfully removed.

        Raises:
            HTTPException: If the like does not exist.
        """
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
        """
        Retrieves analytics data for likes within a specified date range.

        Args:
            date_from (str): The start date in the format 'YYYY-MM-DD'.
            date_to (str): The end date in the format 'YYYY-MM-DD'.

        Returns:
            dict: A dictionary containing likes analytics data.

        Raises:
            HTTPException: If there are no likes within the specified date range.
        """
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
