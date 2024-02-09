from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        """Получение объекта по id"""
        db_obj = await session.execute(select(self.model).where(
            self.model.id == obj_id
        ))
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        """Получаем все объекты модели."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(self, obj_in, session: AsyncSession,
                     user: Optional[User] = None,
                     commit: Optional[bool] = True):
        """Создать объект."""
        obj_in_data = obj_in.dict()
        obj_in_data['invested_amount'] = 0
        if user:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if not commit:
            return db_obj
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj, obj_in,
                     session: AsyncSession):
        """Обновить объект."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj,
                     session: AsyncSession):
        """Удалить объект."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_non_invested(self, session: AsyncSession):
        """Получаем список не инвестированных объектов."""
        db_objs = await session.scalars(select(self.model).where(
            self.model.fully_invested == 0
        ).order_by(self.model.create_date))
        return db_objs.all()
