def classify_transaction(ep: str) -> str:
    classification_map = {
        'PURCHASE ORIGINAL SALE': 'COMPRA',
        'MERCHANDISE CREDIT ORIGINAL SALE': 'COMPRA',
        'ATM CASH ORIGINAL WITHDRAWAL': 'SAQUE',
        'PURCHASE DISPUTE RESP FIN': 'REAPRESENTACAO',
        'PURCHASE DISPUTE RESP FIN REVERSAL': 'REVERSO-DE-REAPRESENTACAO',
        'PURCHASE DISPUTE FIN': 'CHARGEBACK-DE-COMPRA',
        'PURCHASE DISPUTE FIN REVERSAL': 'REVERSO-DE-CHARGEBACK',
        'PURCHASE ORIGINAL SALE REVERSAL': 'REVERSO-DE-COMPRA',
        'ATM CASH REVERSAL': 'REVERSO-DE-SAQUE'
    }

    return classification_map.get(ep)
