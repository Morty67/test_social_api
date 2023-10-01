from app.models import User
import datetime
from app.repositories.base_repository import BaseRepository
from sqlalchemy import update


class UserRepository(BaseRepository):
    model = User

    async def get_user_by_email(self, email: str):
        query = self.model.__table__.select().where(self.model.email == email)
        return await self.get_one(query)

    async def get_user_by_username(self, username: str):
        query = self.model.__table__.select().where(
            self.model.username == username
        )
        return await self.get_one(query)

    async def exists_by_username(self, username: str) -> bool:
        query = self.model.__table__.select().where(
            self.model.username == username
        )
        return await self.exists(query)

    async def exists_by_email(self, email: str) -> bool:
        query = self.model.__table__.select().where(self.model.email == email)
        return await self.exists(query)

    async def get_one(self, query):
        response = await self.session.execute(query)
        result = response.first()
        return result

    async def get_last_login(self, user_id: int):
        query = self.model.__table__.select().where(self.model.id == user_id)
        query = query.with_only_columns(self.model.last_login)
        response = await self.session.execute(query)
        result = response.scalar()
        return result

    async def update_last_login(self, user: User):
        query = (
            update(self.model)
            .where(self.model.id == user.id)
            .values(last_login=datetime.datetime.utcnow())
        )
        await self.session.execute(query)
        await self.session.commit()

    async def get_user_by_id(self, user_id: int):
        query = self.model.__table__.select().where(self.model.id == user_id)
        return await self.get_one(query)

    async def update_last_request(self, user: User):
        query = (
            update(self.model)
            .where(self.model.id == user.id)
            .values(last_request=datetime.datetime.utcnow())
        )
        await self.session.execute(query)
        await self.session.commit()

    async def get_last_request(self, user_id: int):
        query = self.model.__table__.select().where(self.model.id == user_id)
        query = query.with_only_columns(self.model.last_request)
        response = await self.session.execute(query)
        result = response.scalar()
        return result
