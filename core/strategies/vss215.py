from core.strategies import register_strategy
from core.strategies.vss_generic import GenericStrategy


@register_strategy("VSS-215")
class VSS215Strategy(GenericStrategy):
    def __init__(self):
        super().__init__(labels=['INTERCHANGE_AMOUNT', 'INTL_SERVICE_ASSESSMENT', 'AMOUNT', 'ASSESSMENT', 'OPT_ISA_FEE'])
