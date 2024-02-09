from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class ProjectBasicModel(BaseModel):
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        orm_mode = True
