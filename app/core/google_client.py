from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds
from fastapi import HTTPException

from app.constants import INFO

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
CONNECT_ERROR = 'Ошибка ключа доступа к сервисному аккаунту.'


async def get_service():
    if None in INFO.values():
        raise HTTPException(
            status_code=500,
            detail=CONNECT_ERROR
        )
    async with Aiogoogle(
        service_account_creds=ServiceAccountCreds(scopes=SCOPES, **INFO)
    ) as aiogoogle:
        yield aiogoogle
