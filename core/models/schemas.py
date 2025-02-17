from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, validator


class AmountSchema(BaseModel):
    section: str
    label: str
    count: Decimal
    credit_amount: Decimal
    debit_amount: Decimal
    total_amount: Decimal

    @validator('count', 'credit_amount', 'debit_amount', 'total_amount', pre=True)
    def parse_currency(cls, value):
        value_str = str(value).strip()
        is_debit = "DB" in value_str

        # Remove todos os sufixos não numéricos
        clean_value = ''.join([c for c in value_str if c.isdigit() or c in ('.', '-')])

        try:
            decimal_value = Decimal(clean_value)
        except:
            decimal_value = Decimal('0')

        return -decimal_value if is_debit else decimal_value


class ReportSchema(BaseModel):
    report_id: str
    reporting_for: str
    page: Optional[int] = None
    proc_date: datetime
    rollup_to: Optional[str] = None
    report_date: datetime
    funds_xfer_entity: Optional[str] = None
    settlement_currency: str
    summary: List[Optional[str]] = []
    amounts: List[AmountSchema]

    @validator('proc_date', 'report_date', pre=True)
    def parse_dates(cls, value):
        return datetime.strptime(value, "%d%b%y") if value else None

    @validator('*', pre=True)
    def parse_raw(cls, value):
        return value.strip() if isinstance(value, str) else value
