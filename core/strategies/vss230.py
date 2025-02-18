from core.strategies import register_strategy
from core.strategies.vss_generic import GenericStrategy


@register_strategy("VSS-230")
class VSS230Strategy(GenericStrategy):
    def __init__(self):
        super().__init__(labels=['COUNT', 'INTERCHANGE_AMOUNT', 'CREDITS', 'DEBITS'])
