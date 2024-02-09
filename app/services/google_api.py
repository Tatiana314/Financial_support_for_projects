from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

COLUMN = 3
DIMENSION = 'ROWS'
ERROR = (
    'Сохраняемые данные превышают размер таблицы.'
    'Размер таблицы: {} X {}; размер данных: {} X {}.'

)
FORMAT = '%Y/%m/%d %H:%M:%S'
ROW = 100
TABLE_FORMAT = 'USER_ENTERED'
TABLE_NAME = 'Отчёт от {}'
ROLE = 'writer'
TYPE = 'user'
TABLE_HEADER = [
    ['Отчёт от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание'],
]
SPREADSHEET_BODY = dict(
    properties=dict(
        locale="ru_RU"
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Закрытые проекты',
        gridProperties=dict(rowCount=ROW, columnCount=COLUMN),
    ))],
)


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
    spreadsheet_body=deepcopy(SPREADSHEET_BODY)
) -> str:
    """Создание гугл-таблицы с отчётом на диске сервисного аккаунта."""
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body['properties']['title'] = (
        TABLE_NAME.format(datetime.now().strftime(FORMAT))
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetUrl'], response['spreadsheetId']


async def set_user_permissions(
    spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:
    """Разрешение на доступ к гугл-таблице."""
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            fields='id',
            json={'type': TYPE, 'role': ROLE, 'emailAddress': settings.email},
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: list,
    wrapper_services: Aiogoogle,
    sort_key=(lambda obj: obj.timedelta)
) -> None:
    """Обновление данных в гугл-таблице."""
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        *TABLE_HEADER,
        *[list(map(
            str, (project.name, project.timedelta, project.description)
        )) for project in sorted(projects, key=sort_key)]
    ]
    table_values[0][1] = datetime.now().strftime(FORMAT)
    row_table = len(table_values)
    column_table = max(map(len, table_values))
    if row_table > ROW or column_table > COLUMN:
        raise ValueError(ERROR.format(COLUMN, ROW, column_table, row_table))
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f"R1C1:R{row_table}C{column_table}",
            valueInputOption=TABLE_FORMAT,
            json={"majorDimension": DIMENSION, 'values': table_values},
        )
    )
