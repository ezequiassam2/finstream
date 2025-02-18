from core.strategies import register_strategy
from core.strategies.vss_generic import GenericStrategy


@register_strategy("VSS-910")
class VSS910Strategy(GenericStrategy):
    def __init__(self):
        super().__init__(labels=['COUNT', 'TRANSACTION_AMOUNT', 'INTERCHANGE_FEE', 'PAYMENT_AMOUNT'])
