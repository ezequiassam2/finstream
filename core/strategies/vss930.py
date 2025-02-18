from core.strategies import register_strategy
from core.strategies.vss_generic import GenericStrategy


@register_strategy("VSS-930")
class VSS930Strategy(GenericStrategy):
    def __init__(self):
        super().__init__(labels=['COUNT', 'INTERCHANGE_AMOUNT', 'CREDITS_FEE', 'DEBITS_FEE'])
