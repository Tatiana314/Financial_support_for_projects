from sqlalchemy import Column, String, Text
from sqlalchemy.ext.hybrid import hybrid_property

from app.constants import MAX_LEN
from app.models.base import InvestmentBasicModel

DATA = '{name}, {description:.15}, {base}'


class CharityProject(InvestmentBasicModel):
    """Модель проекта."""
    name = Column(String(MAX_LEN), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return DATA.format(
            name=self.name,
            description=self.description,
            base=super().__repr__()
        )

    @hybrid_property
    def timedelta(self):
        return (self.close_date - self.create_date)
