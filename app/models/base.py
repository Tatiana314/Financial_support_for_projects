"""
Описание абстрактной модели.
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy import CheckConstraint

from app.core.db import Base

DATA = ('{id}, объем инвестиций: {full_amount}, '
        'инвестированная сумма: {invested_amount}, '
        'инвестированно: {fully_invested}, '
        'дата создания: {create_date}, '
        'дата закрытия: {close_date}')


class InvestmentBasicModel(Base):
    """Абстрактная модель."""
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0'), CheckConstraint('full_amount >= invested_amount')
    )
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime)

    def __repr__(self):
        return DATA.format(
            id=self.id,
            full_amount=self.full_amount,
            invested_amount=self.invested_amount,
            fully_invested=self.fully_invested,
            create_date=self.create_date,
            close_date=self.close_date
        )
