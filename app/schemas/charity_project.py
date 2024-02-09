from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, validator

from app.constants import MAX_LEN, MIN_LEN
from app.schemas.base import ProjectBasicModel

ERROR = 'Имя проекта не может быть пустым!'


class CharityProjectBasic(BaseModel):
    """Базовая Pydantic-схема."""
    name: str = Field(..., min_length=MIN_LEN, max_length=MAX_LEN)
    description: str = Field(..., min_length=MIN_LEN)


class CharityProjectDB(ProjectBasicModel, CharityProjectBasic):
    """Pydantic-схема объекта из БД."""


class CharityProjectCreate(CharityProjectBasic):
    """Pydantic-схема создания объекта."""
    full_amount: PositiveInt


class CharityProjectUpdate(BaseModel):
    """Pydantic-схема обновление объекта."""
    name: Optional[str] = Field(None, min_length=MIN_LEN, max_length=MAX_LEN)
    description: Optional[str] = Field(None, min_length=MIN_LEN)
    full_amount: Optional[PositiveInt]

    class Config(ProjectBasicModel.Config):
        pass

    @validator('name')
    def validator_name(cls, value: str) -> str:
        if value:
            return value
        raise ValueError(ERROR)
