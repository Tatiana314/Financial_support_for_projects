from datetime import datetime

from app.models.base import InvestmentBasicModel


def investment_process(
    target: InvestmentBasicModel,
    sources: list[InvestmentBasicModel]
) -> list[InvestmentBasicModel]:
    """Инвестирование в проект."""
    updated_sources = []
    for source in sources:
        invest = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += invest
            if obj.full_amount == obj.invested_amount:
                obj.fully_invested = True
                obj.close_date = datetime.utcnow()
        updated_sources.append(source)
        if target.fully_invested:
            break
    return updated_sources
