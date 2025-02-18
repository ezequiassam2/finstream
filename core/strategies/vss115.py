from core.strategies import register_strategy
from core.strategies.vss_generic import GenericStrategy


@register_strategy("VSS-115")
class VSS115Strategy(GenericStrategy):
    def __init__(self):
        super().__init__(labels=['credit_count', 'credit_amount', 'debit_count', 'debit_amount', 'total_count', 'total_amount'])
