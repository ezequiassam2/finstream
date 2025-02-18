from core.strategies import register_strategy
from core.strategies.vss_generic import GenericStrategy


@register_strategy("VSS-135")
class VSS135Strategy(GenericStrategy):
    def __init__(self):
        super().__init__(labels=['count', 'interchange_amount', 'reimbursement_fees', 'count_amount', 'interchange_fees', 'reimbursement'])
