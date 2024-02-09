from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):
    async def get_all_user_donations(
        self, session: AsyncSession, user_id: int
    ):
        """Получение всех пожертвований текущего пользователя."""
        db_objs = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        return db_objs.scalars().all()


donation = CRUDDonation(Donation)
