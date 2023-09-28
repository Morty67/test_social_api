from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select, insert
from sqlalchemy import delete


class BaseRepository:
    model: Any = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, new_obj: dict):
        query = insert(self.model).returning(self.model)
        response = await self.session.execute(query, new_obj)
        await self.session.commit()
        new_obj = response.scalar()
        return new_obj

    async def exists(self, query: Select):
        query = query.with_only_columns(self.model.id)
        response = await self.session.execute(query)

        result = response.first()
        return bool(result)

    async def get_one(self, query: Select):
        response = await self.session.execute(query)
        result = response.first()
        return result

    async def delete(self, obj_id: int):
        query = delete(self.model).where(self.model.id == obj_id)
        await self.session.execute(query)
        await self.session.commit()

    async def save(self, obj: Any):
        self.session.add(obj)
        await self.session.commit()
