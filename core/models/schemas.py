from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional, Dict

from pydantic import BaseModel, validator


class AmountSchema(BaseModel): #todo: adicionar classificação de transação .php considerando a junção do section e label
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
    clearing_debit: int
    installment_nbr: int
    clearing_installment: int
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
    clearing_boarding_fee: int
    clearing_settlement_date: date
    clearing_presentation: int
    clearing_action_code: int
    clearing_total_partial_transaction: int
    clearing_flag_partial_settlement: int
    clearing_cancel: int
    clearing_confirm: int
    clearing_add: int
    clearing_credit: int
    transaction_type: Optional[str] = None
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

    @validator('transaction_type', always=True)
    def classify_transaction(cls, v, values):
        slice_code = values.get('slice_code', '')
        clearing_action_code = values.get('clearing_action_code', '')
        operation_code = values.get('operation_code', '')
        clearing_cancel = values.get('clearing_cancel', 0)
        clearing_interchange_fee_sign = values.get('clearing_interchange_fee_sign', '')
        operation_type = values.get('operation_type', 0)
        clearing_debit = values.get('clearing_debit', False)
        reason_code = values.get('reason_code', '')

        if not slice_code:
            return 'UNKNOWN'
        if clearing_action_code == 11 and not operation_code and clearing_cancel == 1 and clearing_interchange_fee_sign == 'D':
            return 'REVERSO-DE-COMPRA'
        if operation_type == 1 and not operation_code:
            return 'REVERSO-DE-SAQUE'
        if operation_type in ('0', '1') and operation_code == '02':
            return 'SAQUE' if clearing_debit else 'REVERSO-DE-SAQUE'
        if operation_code == '01' and reason_code < '2000':
            return 'REVERSO-DE-COMPRA' if not clearing_debit else 'COMPRA'
        return 'UNKNOWN-99'
