from sqlalchemy import select

from app.models import Post, User
from app.repositories.base_repository import BaseRepository


class PostRepository(BaseRepository):
    model = Post

    async def get_posts_by_user_id(self, user_id: int):
        query = self.model.__table__.select().where(
            self.model.user_id == user_id
        )
        return await self.session.execute(query).scalars().all()

    async def get_user_by_id(self, user_id: int):
        query = select(User).where(User.id == user_id)
        response = await self.session.execute(query)
        user = response.scalar()
        return user

    async def get_post_by_id(self, post_id: int):
        query = self.model.__table__.select().where(self.model.id == post_id)
        return await self.get_one(query)
