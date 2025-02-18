from core.strategies import register_strategy
from core.strategies.vss_generic import GenericStrategy


@register_strategy("VSS-900")
class VSS900Strategy(GenericStrategy):
    def __init__(self):
        super().__init__(index_insert_last=True, labels=['COUNT', 'CLEARING_AMOUNT', 'TOTAL_COUNT_AMOUNT'])
