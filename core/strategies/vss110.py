from core.strategies import register_strategy
from core.strategies.vss_generic import GenericStrategy


@register_strategy("VSS-110")
class VSS110Strategy(GenericStrategy):
    def __init__(self):
        super().__init__()
