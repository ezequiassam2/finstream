from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional, Dict

from pydantic import BaseModel, validator


class AmountSchema(BaseModel):
    section: str
    label: str
    processing_date: Optional[datetime] = None
    processing_count: Optional[Decimal] = None
    transaction_amount: Optional[Decimal] = None
    interchange_fee: Optional[Decimal] = None
    processing_charge: Optional[Decimal] = None
    settlement_amount: Optional[Decimal] = None
    data: Optional[Dict] = {}

    @validator('processing_count', 'transaction_amount', 'interchange_fee', 'processing_charge', 'settlement_amount',
               pre=True)
    def parse_currency(cls, value):
        if value is None:
            return None
        value_str = str(value).strip()
        is_debit = "DB" in value_str

        # Remove all non-numeric suffixes
        clean_value = ''.join([c for c in value_str if c.isdigit() or c in ('.', '-')])

        try:
            decimal_value = Decimal(clean_value)
        except:
            decimal_value = Decimal('0')

        return -decimal_value if is_debit else decimal_value

    @validator('processing_date', pre=True)
    def parse_dates(cls, value):
        return datetime.strptime(value, "%d%b%y") if value else None

    @validator('data', pre=True)
    def validate_data(cls, value):
        if isinstance(value, dict):
            for k, v in value.items():
                if any(char.isdigit() for char in str(v)):
                    value[k] = float(cls.parse_currency(v))
        return value

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


#todo: fazer validação para add transaction_type
class TransactionSchema(BaseModel):
    source: str
    source_date: date
    dest_currency: int
    arn: str
    slice_code: str
    cardbrandid: str
    externalid: str
    local_date: date
    authorization_date: Optional[date] = None
    purchase_value: Decimal
    clearing_debit: Decimal
    installment_nbr: Decimal
    clearing_installment: Decimal
    installment_value_1: Decimal
    installment_value_n: Decimal
    clearing_value: Decimal
    issuer_exchange_rate: Decimal
    clearing_commission: Decimal
    clearing_interchange_fee_sign: str
    qualifier: str
    bin_card: str
    acquirer_id: int
    mcc: int
    dest_value: Decimal
    boarding_fee: Decimal
    status: int
    operation_type: str
    cdt_amount: Decimal
    product_code: str
    operation_code: str
    reason_code: str
    pan: str
    late_presentation: int
    entry_mode: str
    pos_entry_mode: str
    clearing_files_row_id: int
    clearing_currency: int
    clearing_boarding_fee: Decimal
    clearing_settlement_date: date
    clearing_presentation: Decimal
    clearing_action_code: Decimal
    clearing_total_partial_transaction: Decimal
    clearing_flag_partial_settlement: Decimal
    clearing_cancel: Decimal
    clearing_confirm: Decimal
    clearing_add: Decimal
    clearing_credit: Decimal
    section_num: int
    raw: Dict = {}

    @validator('*', pre=True)
    def parse_raw(cls, value):
        return value.strip() if isinstance(value, str) else value

    @validator('source_date', 'local_date',  'authorization_date',  'clearing_settlement_date', pre=True)
    def parse_date(cls, value):
        return datetime.strptime(value, "%Y-%m-%d").date() if value else None

    @validator('raw')
    def convert_decimals(cls,value):
        if isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, Decimal):
                    value[k] = float(v)
        return value