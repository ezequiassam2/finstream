import pytest
from core.strategies.vss110 import VSS110Strategy

def test_vss110_parsing():
    strategy = VSS110Strategy()
    sample_content = """  
    REPORT ID:  VSS-110  
    REPORTING FOR: 2023-10  
    *** INTERCHANGE VALUE ***  
    TOTAL ISSUER               334,544       350,719.10     28,432,638.49     28,081,919.39DB  
    """
    header = strategy.parse_header(sample_content)
    assert header.report_id == "VSS-110"
    amounts = strategy.parse_amounts(sample_content)
    assert amounts[0].total_amount == Decimal("-28081919.39")
