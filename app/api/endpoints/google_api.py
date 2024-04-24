from http import HTTPStatus

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.crud.charity_project import charity_project
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)

POST_DESC = 'Получить отчёт в гугл-таблице.'

router = APIRouter()


@router.get('/', description=POST_DESC)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await charity_project.get_projects_by_completion_rate(
        session
    )
    spreadsheet_url, spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(
            spreadsheet_id, projects, wrapper_services
        )
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(error))
    return spreadsheet_url
