from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate

MIN_LEN_PASSWORD = 3
LEN_ERROR = 'Password should be at least 3 characters'
PASSWORD_ERROR = 'Password should not contain e-mail'
REPORT = 'Пользователь {email} зарегистрирован.'
LIFETIME = 3600
TOKEN_URL = 'auth/jwt/login'


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

bearer_transport = BearerTransport(tokenUrl=TOKEN_URL)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=LIFETIME)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < MIN_LEN_PASSWORD:
            raise InvalidPasswordException(
                reason=LEN_ERROR
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason=PASSWORD_ERROR
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        print(REPORT.format(email=user.email))


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
