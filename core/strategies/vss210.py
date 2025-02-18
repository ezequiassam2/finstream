from core.strategies import register_strategy
from core.strategies.vss_generic import GenericStrategy


@register_strategy("VSS-210")
class VSS210Strategy(GenericStrategy):
    def __init__(self):
        super().__init__(labels=['AMOUNT', 'CONVERSION_FEE', 'INTERCHANGE_AMOUNT', 'CONVERSION_FEE', 'OPT_ISSUER_FEE'])
