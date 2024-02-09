from datetime import datetime
from aiogoogle import Aiogoogle
from fastapi import HTTPException

from app.constants import ROW
from app.core.config import settings

COLUMN = 3
CONNECT_ERROR = 'Ошибка доступа к гугл-таблице.'
DIMENSION = 'ROWS'
FORMAT = '%Y/%m/%d %H:%M:%S'
TABLE_FORMAT = 'USER_ENTERED'
TABLE_NAME = 'Отчёт от {}'
SHEET_NAME = 'Закрытые проекты'
SHEET_TYPE = 'GRID'
LOCAL = 'ru_RU'
SHEET_ID = 0
ROLE = 'writer'
TYPE = 'user'
TABLE_HEADER = [
        ['Отчёт от',],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создание гугл-таблицы с отчётом на диске сервисного аккаунта."""
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': TABLE_NAME.format(datetime.now().strftime(FORMAT)),
                       'locale': LOCAL},
        'sheets': [{'properties': {'sheetType': SHEET_TYPE,
                                   'sheetId': SHEET_ID,
                                   'title': SHEET_NAME,
                                   'gridProperties': {'rowCount': ROW,
                                                      'columnCount': COLUMN}}}]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """Разрешение на доступ к гугл-таблице."""
    if not settings.email:
        raise HTTPException(
            status_code=500,
            detail=CONNECT_ERROR
        )
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            fields='id',
            json={
                'type': TYPE,
                'role': ROLE,
                'emailAddress': settings.email
        }))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """Обновление данных в гугл-таблице."""
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = TABLE_HEADER
    table_values[0].append(datetime.now().strftime(FORMAT))
    for project in projects:
        table_values.append(list(map(str, [
            project.name, project.timedelta, project.description
        ])))
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:{chr(64 + max(map(len, table_values)))}{len(table_values)}',
            valueInputOption=TABLE_FORMAT,
            json={
                'majorDimension': DIMENSION,
                'values': table_values
            }))
