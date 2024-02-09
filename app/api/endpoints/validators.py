from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.charity_project import charity_project
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate

CLOSED_PROJECT = 'Закрытый проект нельзя редактировать!'
DELETION_ERROR = 'В проект были внесены средства, не подлежит удалению!'
INVEST_ERROR = 'Требуемая сумма не может быть меньше внесенной суммы.'
NAME_ERROR = 'Проект с таким именем уже существует!'
NO_OBJECT = 'Объект не найден.'
STATUS_CODE = 400


async def check_charity_project_removal(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Нельзя удалить проект, в который уже были
    инвестированы средства, его можно только закрыть."""
    result = await session.execute(select(CharityProject).where(
        CharityProject.id == project_id,
        CharityProject.invested_amount == 0
    ))
    result = result.scalars().first()
    if result:
        return result
    raise HTTPException(
        status_code=STATUS_CODE,
        detail=DELETION_ERROR
    )


async def check_charity_project_update(
        project: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession,
):
    """Валидация данных перед обновлением проекта."""
    if not project:
        raise HTTPException(
            status_code=STATUS_CODE,
            detail=NO_OBJECT
        )
    if project.fully_invested:
        raise HTTPException(
            status_code=STATUS_CODE,
            detail=CLOSED_PROJECT
        )
    if obj_in.full_amount and obj_in.full_amount < project.invested_amount:
        raise HTTPException(
            status_code=STATUS_CODE,
            detail=INVEST_ERROR
        )
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверка на уникальность названия проекта."""
    if await charity_project.get_project_id_by_name(project_name, session):
        raise HTTPException(
            status_code=STATUS_CODE,
            detail=NAME_ERROR,
        )
