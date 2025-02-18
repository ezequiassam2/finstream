from core.strategies import register_strategy
from core.strategies.vss_generic import GenericStrategy


@register_strategy("VSS-120")
class VSS120Strategy(GenericStrategy):
    def __init__(self):
        super().__init__(labels=['count', 'credit_amount', 'debit_value', 'interchange_value'])
