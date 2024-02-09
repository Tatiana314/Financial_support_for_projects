from sqlalchemy import Column, Integer, ForeignKey, Text
from app.models.base import InvestmentBasicModel

DATA = '{user_id}, {comment:.15}, {base}'


class Donation(InvestmentBasicModel):
    """Модель пожертвования."""
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        super().__repr__()
        return DATA.format(
            user_id=self.user_id,
            comment=self.comment,
            base=super().__repr__()
        )
