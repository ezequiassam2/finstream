from core.strategies import register_strategy
from core.strategies.vss_generic import GenericStrategy


@register_strategy("VSS-610")
class VSS610Strategy(GenericStrategy):
    def __init__(self):
        super().__init__(labels=['PROCESSING_DATE', 'COUNT', 'TRANSACTION_AMOUNT', 'INTERCHANGE_FEE'])
