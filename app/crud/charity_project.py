from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.constants import ROW

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Получение объекта по названию."""
        db_project_id = await session.execute(
            select(CharityProject.id)
            .where(CharityProject.name == project_name)
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
            sort_key=(lambda obj: obj.timedelta)
    ) -> list:
        """
        Закрытые проекты, отсортированные
        по скорости сбора средств.
        """
        projects = await session.scalars(
            select(CharityProject)
            .where(CharityProject.fully_invested == True).limit(ROW)
        )
        return sorted(projects.all(), key=sort_key)


charity_project = CRUDCharityProject(CharityProject)
