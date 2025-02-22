-- SOMA TOTAL DE COMPRA EM BRL
SELECT SUM(CASE
               WHEN r.report_id = 'VSS-120'
                   THEN CAST(a.data ->> 'credit_amount' AS NUMERIC)
               WHEN r.report_id = 'VSS-600'
                   THEN a.transaction_amount
               WHEN r.report_id = 'VSS-910'
                   THEN CAST(a.data ->> 'transaction_amount' AS NUMERIC)
               ELSE 0
    END) AS total_compras_brl
FROM reports as r
         INNER JOIN amounts a ON r.id = a.report_id
WHERE r.settlement_currency = 'BRL'
  AND a.transaction_class = 'COMPRA';

-- SOMA TOTAL DE COMPRA EM USD
SELECT SUM(CASE
               WHEN r.report_id = 'VSS-120'
                   THEN CAST(a.data ->> 'credit_amount' AS NUMERIC)
               WHEN r.report_id = 'VSS-600'
                   THEN a.transaction_amount
               WHEN r.report_id = 'VSS-910'
                   THEN CAST(a.data ->> 'transaction_amount' AS NUMERIC)
               ELSE 0
    END) AS total_compras_usd
FROM reports as r
         INNER JOIN amounts a ON r.id = a.report_id
WHERE r.settlement_currency = 'USD'
  AND a.transaction_class = 'COMPRA';

-- SOMA TOTAL DE SAQUE EM BRL
SELECT SUM(CASE
               WHEN r.report_id = 'VSS-120'
                   THEN CAST(a.data ->> 'debit_value' AS NUMERIC)
               WHEN r.report_id = 'VSS-600'
                   THEN a.settlement_amount
               WHEN r.report_id = 'VSS-910'
                   THEN CAST(a.data ->> 'payment_amount' AS NUMERIC)
               ELSE 0
    END) AS total_saque_brl
FROM reports as r
         INNER JOIN amounts a ON r.id = a.report_id
WHERE r.settlement_currency = 'BRL'
  AND a.transaction_class = 'SAQUE';

-- SOMA TOTAL DE SAQUE USD
SELECT SUM(CASE
               WHEN r.report_id = 'VSS-120'
                   THEN CAST(a.data ->> 'debit_value' AS NUMERIC)
               WHEN r.report_id = 'VSS-600'
                   THEN a.settlement_amount
               WHEN r.report_id = 'VSS-910'
                   THEN CAST(a.data ->> 'payment_amount' AS NUMERIC)
               ELSE 0
    END) AS total_saque_usd
FROM reports as r
         INNER JOIN amounts a ON r.id = a.report_id
WHERE r.settlement_currency = 'USD'
  AND a.transaction_class = 'SAQUE';


-- SOMA TOTAL DE REPASSE LÍQUIDO EM BRL
SELECT SUM(CASE
               WHEN a.transaction_class IN
                    ('COMPRA', 'SAQUE', 'REVERSO-DE-REAPRESENTACAO', 'CHARGEBACK-DE-COMPRA')
                   THEN CASE
                            WHEN r.report_id = 'VSS-120'
                                THEN CAST(a.data ->> 'credit_amount' AS NUMERIC)
                            WHEN r.report_id = 'VSS-600'
                                THEN a.transaction_amount
                            WHEN r.report_id = 'VSS-910'
                                THEN CAST(a.data ->> 'transaction_amount' AS NUMERIC)
                   END
               ELSE 0
    END) - SUM(CASE
                   WHEN a.transaction_class IN
                        ('REAPRESENTACAO', 'REAPRESENTACAO', 'REVERSO-DE-COMPRA', 'REVERSO-DE-SAQUE')
                       THEN CASE
                                WHEN r.report_id = 'VSS-120'
                                    THEN CAST(a.data ->> 'debit_value' AS NUMERIC)
                                WHEN r.report_id = 'VSS-600'
                                    THEN a.settlement_amount
                                WHEN r.report_id = 'VSS-910'
                                    THEN CAST(a.data ->> 'payment_amount' AS NUMERIC)
                       END
                   ELSE 0
    END) AS total_repasse_liquido_brl
FROM reports as r
         INNER JOIN amounts a ON r.id = a.report_id
WHERE r.settlement_currency = 'BRL'
  AND a.transaction_class IS NOT NULL;


-- SOMA TOTAL DE REPASSE LÍQUIDO EM USD
SELECT SUM(CASE
               WHEN a.transaction_class IN
                    ('COMPRA', 'SAQUE', 'REVERSO-DE-REAPRESENTACAO', 'CHARGEBACK-DE-COMPRA')
                   THEN CASE
                            WHEN r.report_id = 'VSS-120'
                                THEN CAST(a.data ->> 'credit_amount' AS NUMERIC)
                            WHEN r.report_id = 'VSS-600'
                                THEN a.transaction_amount
                            WHEN r.report_id = 'VSS-910'
                                THEN CAST(a.data ->> 'transaction_amount' AS NUMERIC)
                   END
               ELSE 0
    END) - SUM(CASE
                   WHEN a.transaction_class IN
                        ('REAPRESENTACAO', 'REAPRESENTACAO', 'REVERSO-DE-COMPRA', 'REVERSO-DE-SAQUE')
                       THEN CASE
                                WHEN r.report_id = 'VSS-120'
                                    THEN CAST(a.data ->> 'debit_value' AS NUMERIC)
                                WHEN r.report_id = 'VSS-600'
                                    THEN a.settlement_amount
                                WHEN r.report_id = 'VSS-910'
                                    THEN CAST(a.data ->> 'payment_amount' AS NUMERIC)
                       END
                   ELSE 0
    END) AS total_repasse_liquido_usd
FROM reports as r
         INNER JOIN amounts a ON r.id = a.report_id
WHERE r.settlement_currency = 'USD'
  AND a.transaction_class IS NOT NULL;

-- ****ARQUIVOS DE CLEARING******

-- CLEARING - SOMA TOTAL DE COMPRA EM BRL
SELECT SUM(purchase_value) AS total_compras_brl
FROM transactions
WHERE dest_currency = 986
  AND transaction_type = 'COMPRA';

-- CLEARING - SOMA TOTAL DE COMPRA EM USD
SELECT SUM(purchase_value) AS total_compras_usd
FROM transactions
WHERE dest_currency = 840
  AND transaction_type = 'COMPRA';

-- CLEARING - SOMA TOTAL DE SAQUE EM BRL
SELECT SUM(purchase_value) AS total_saque_brl
FROM transactions
WHERE dest_currency = 986
  AND transaction_type = 'SAQUE';

-- CLEARING - SOMA TOTAL DE SAQUE EM USD
SELECT SUM(purchase_value) AS total_saque_usd
FROM transactions
WHERE dest_currency = 840
  AND transaction_type = 'SAQUE';


-- CLEARING - SOMA TOTAL DE REPASSE LÍQUIDO EM BRL
SELECT SUM(CASE
               WHEN transaction_type IN ('REVERSO-DE-COMPRA', 'REVERSO-DE-SAQUE') THEN clearing_value
               WHEN transaction_type IN ('COMPRA', 'SAQUE') THEN -clearing_value
               ELSE 0
    END) AS repasse_liquido_brl
FROM transactions
WHERE dest_currency = 986;


-- CLEARING - SOMA TOTAL DE REPASSE LÍQUIDO EM USD
SELECT SUM(CASE
               WHEN transaction_type IN ('REVERSO-DE-COMPRA', 'REVERSO-DE-SAQUE') THEN clearing_value
               WHEN transaction_type IN ('COMPRA', 'SAQUE') THEN -clearing_value
               ELSE 0
    END) AS repasse_liquido_brl
FROM transactions
WHERE dest_currency = 840;