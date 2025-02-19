
from sqlalchemy import Column, Integer, String, DateTime,Date, ForeignKey, DECIMAL, JSON, Index, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ModelRepository(Base):
    __abstract__ = True
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

class Report(ModelRepository):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    report_id = Column(String(50), index=True)
    reporting_for = Column(String, index=True)
    page = Column(Integer)
    proc_date = Column(DateTime, index=True)
    rollup_to = Column(String)
    report_date = Column(DateTime, index=True)
    funds_xfer_entity = Column(String)
    settlement_currency = Column(String(3), index=True)
    summary = Column(JSON)
    file_segment = Column(Integer)
    content_raw = Column(String)
    amounts = relationship("Amount", back_populates="report", cascade="all, delete-orphan")


class Amount(ModelRepository):
    __tablename__ = 'amounts'
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('reports.id', ondelete="CASCADE"), index=True)
    section = Column(String, index=True)
    label = Column(String)
    processing_date = Column(DateTime, index=True)
    processing_count = Column(DECIMAL(18, 2))
    transaction_amount = Column(DECIMAL(18, 2))
    interchange_fee = Column(DECIMAL(18, 2))
    processing_charge = Column(DECIMAL(18, 2))
    settlement_amount = Column(DECIMAL(18, 2))
    data = Column(JSON)
    report = relationship("Report", back_populates="amounts")

class Transaction(ModelRepository):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    source = Column(String(50), nullable=False)
    source_date = Column(Date, nullable=False, index=True)
    dest_currency = Column(Integer, nullable=False)
    arn = Column(String, unique=True, index=True)
    slice_code = Column(String, index=True)
    cardbrandid = Column(String)
    externalid = Column(String)
    local_date = Column(Date)
    authorization_date = Column(Date)
    purchase_value = Column(DECIMAL(18, 2), nullable=False)
    clearing_debit = Column(DECIMAL(18, 2))
    installment_nbr = Column(DECIMAL(18, 2))
    clearing_installment = Column(DECIMAL(18, 2))
    installment_value_1 = Column(DECIMAL(18, 2))
    installment_value_n = Column(DECIMAL(18, 2))
    clearing_value = Column(DECIMAL(18, 2))
    issuer_exchange_rate = Column(DECIMAL(18, 6))
    clearing_commission = Column(DECIMAL(18, 6))
    clearing_interchange_fee_sign = Column(String)
    qualifier = Column(String)
    bin_card = Column(String)
    acquirer_id = Column(Integer)
    mcc = Column(Integer, index=True)
    dest_value = Column(DECIMAL(18, 2))
    boarding_fee = Column(DECIMAL(18, 6))
    status = Column(Integer)
    operation_type = Column(String)
    cdt_amount = Column(DECIMAL(18, 2))
    product_code = Column(String)
    operation_code = Column(String)
    reason_code = Column(String)
    pan = Column(String)
    late_presentation = Column(Integer)
    entry_mode = Column(String)
    pos_entry_mode = Column(String)
    clearing_files_row_id = Column(Integer)
    clearing_currency = Column(Integer)
    clearing_boarding_fee = Column(DECIMAL(18, 2))
    clearing_settlement_date = Column(Date)
    clearing_presentation = Column(DECIMAL(18, 2))
    clearing_action_code = Column(DECIMAL(18, 2))
    clearing_total_partial_transaction = Column(DECIMAL(18, 2))
    clearing_flag_partial_settlement = Column(DECIMAL(18, 2))
    clearing_cancel = Column(DECIMAL(18, 2))
    clearing_confirm = Column(DECIMAL(18, 2))
    clearing_add = Column(DECIMAL(18, 2))
    clearing_credit = Column(DECIMAL(18, 2))
    line_segment = Column(Integer)
    content_raw = Column(JSON)


# Índices compostos
Index('idx_report_section', Amount.section)
Index('idx_report_date_currency', Report.report_date, Report.settlement_currency)
Index('idx_transaction_source_currency', Transaction.source, Transaction.dest_currency),
Index('idx_transaction_dates', Transaction.source_date, Transaction.local_date)
