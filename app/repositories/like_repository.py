from sqlalchemy import delete, select, and_, func

from app.models import Like
from app.repositories.base_repository import BaseRepository


class LikeRepository(BaseRepository):
    model = Like

    async def create_like(self, user_id: int, post_id: int):
        like_data = {"user_id": user_id, "post_id": post_id, "is_liked": True}
        return await self.create(like_data)

    async def delete_like(self, user_id: int, post_id: int):
        query = delete(Like).where(
            Like.user_id == user_id, Like.post_id == post_id
        )
        await self.session.execute(query)
        await self.session.commit()

    async def get_like(self, user_id: int, post_id: int):
        query = select(Like).filter(
            Like.user_id == user_id, Like.post_id == post_id
        )
        return await self.get_one(query)

    async def get_likes_in_date_range(self, date_from, date_to):
        query = select(self.model).filter(
            and_(
                func.date(self.model.created_at) >= date_from,
                func.date(self.model.created_at) <= date_to,
            )
        )
        response = await self.session.execute(query)
        likes = response.scalars().all()
        return likes
