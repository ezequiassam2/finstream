from core.strategies import register_strategy
from core.strategies.vss_generic import GenericStrategy


@register_strategy("VSS-140")
class VSS140Strategy(GenericStrategy):
    def __init__(self):
        super().__init__(labels=['count', 'interchange_amount', 'credits', 'debits'])
