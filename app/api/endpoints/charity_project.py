from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import (check_charity_project_removal,
                                          check_charity_project_update,
                                          check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project
from app.crud.donation import donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.service import investment_process

GET_DESC = 'Получает список всех проектов.'
POST_DESC = 'Создает благотворительный проект.'
DELETE_DESC = (
    'Удаляет проект. Нельзя удалить проект, в который '
    'уже были инвестированы средства, его можно только закрыть.'
)
PATCH_DESC = (
    'Закрытый проект нельзя редактировать, также нельзя '
    'установить требуемую сумму меньше уже вложенной.'
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    description=GET_DESC
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    description=POST_DESC,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    obj_data: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(obj_data.name, session)
    project = await charity_project.create(obj_data, session, commit=False)
    session.add_all(investment_process(
        sources=await donation.get_non_invested(session), target=project
    ))
    await session.commit()
    await session.refresh(project)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    description=DELETE_DESC,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    return await charity_project.remove(
        db_obj=await check_charity_project_removal(project_id, session),
        session=session
    )


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    description=PATCH_DESC,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await charity_project.get(project_id, session)
    await check_charity_project_update(project, obj_data, session)
    await charity_project.update(project, obj_data, session)
    return project
