from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project
from app.crud.donation import donation
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationGet
from app.services.service import investment_process

GET_DESC = 'Получает список всех пожертвований.'
GET_USER_DESC = 'Получить список моих пожертвований.'
POST_DESC = 'Сделать пожертвование.'

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    description=GET_DESC
)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    return await donation.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationGet],
    description=GET_USER_DESC
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Только для текущего пользователя."""
    return await donation.get_all_user_donations(
        session=session, user_id=user.id
    )


@router.post(
    '/',
    response_model=DonationGet,
    response_model_exclude_none=True,
    description=POST_DESC
)
async def create_donations(
    obj_data: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Только для зарегистрированных пользователей."""
    new_donation = await donation.create(obj_data, session, user, commit=False)
    session.add_all(investment_process(
        sources=await charity_project.get_non_invested(session), target=new_donation
    ))
    await session.commit()
    await session.refresh(new_donation)
    return new_donation
