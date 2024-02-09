from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt

from app.schemas.base import ProjectBasicModel


class DonationDB(ProjectBasicModel):
    """Pydantic-схема объекта из БД."""
    user_id: int
    comment: Optional[str]


class DonationCreate(BaseModel):
    """Pydantic-схема создания объекта."""
    full_amount: PositiveInt
    comment: Optional[str]

    class Config(ProjectBasicModel.Config):
        pass


class DonationGet(DonationCreate):
    """Pydantic-схема для пользователя."""
    id: int
    create_date: datetime
