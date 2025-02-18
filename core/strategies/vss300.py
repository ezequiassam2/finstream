from core.strategies import register_strategy
from core.strategies.vss_generic import GenericStrategy


@register_strategy("VSS-300")
class VSS300Strategy(GenericStrategy):
    def __init__(self):
        super().__init__(labels=['COUNT', 'INTERCHANGE_VALUE', 'REIMBURSEMENT_CHARGES', 'VISA_AMOUNT', 'SETTLEMENT'])
