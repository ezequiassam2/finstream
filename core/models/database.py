from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, DECIMAL, JSON, Index, func, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ModelRepository(Base):
    __abstract__ = True
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

class Report(ModelRepository):
    __tablename__ = 'reports'
    id = Column(BigInteger, primary_key=True)
    report_id = Column(String(50), index=True)
    reporting_for = Column(String, index=True)
    page = Column(Integer, index=True)
    proc_date = Column(DateTime, index=True)
    rollup_to = Column(String)
    report_date = Column(DateTime, index=True)
    funds_xfer_entity = Column(String)
    settlement_currency = Column(String(3), index=True)
    summary = Column(JSON)
    section_num = Column(Integer, index=True)
    raw = Column(String)
    amounts = relationship("Amount", back_populates="report", cascade="all, delete-orphan")


class Amount(ModelRepository):
    __tablename__ = 'amounts'
    id = Column(BigInteger, primary_key=True)
    report_id = Column(Integer, ForeignKey('reports.id', ondelete="CASCADE"), index=True)
    transaction_class = Column(String, index=True)
    section = Column(String, index=True)
    label = Column(String)
    processing_date = Column(DateTime, index=True)
    processing_count = Column(DECIMAL(18, 2))
    transaction_amount = Column(DECIMAL(18, 2))
    interchange_fee = Column(DECIMAL(18, 2))
    processing_charge = Column(DECIMAL(18, 2))
    settlement_amount = Column(DECIMAL(18, 2))
    data = Column(JSON)
    index = Column(Integer)
    report = relationship("Report", back_populates="amounts")

class Transaction(ModelRepository):
    __tablename__ = 'transactions'
    id = Column(BigInteger, primary_key=True)
    source = Column(String(50), nullable=False)
    source_date = Column(Date, nullable=False, index=True)
    dest_currency = Column(Integer, nullable=False, index=True)
    arn = Column(String, index=True)
    slice_code = Column(String, index=True)
    cardbrandid = Column(String)
    externalid = Column(String)
    local_date = Column(Date, index=True)
    authorization_date = Column(Date, index=True)
    purchase_value = Column(DECIMAL(18, 2), nullable=False)
    clearing_debit = Column(Integer)
    installment_nbr = Column(Integer)
    clearing_installment = Column(Integer)
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
    clearing_boarding_fee = Column(Integer)
    clearing_settlement_date = Column(Date)
    clearing_presentation = Column(Integer)
    clearing_action_code = Column(Integer)
    clearing_total_partial_transaction = Column(Integer)
    clearing_flag_partial_settlement = Column(Integer)
    clearing_cancel = Column(Integer)
    clearing_confirm = Column(Integer)
    clearing_add = Column(Integer)
    clearing_credit = Column(Integer)
    transaction_type = Column(String, index=True)
    section_num = Column(Integer)
    raw = Column(JSON)


# Índices compostos
Index('idx_report_section', Amount.section)
Index('idx_report_date_currency', Report.report_date, Report.settlement_currency)
Index('idx_transaction_source_currency', Transaction.source, Transaction.dest_currency),
Index('idx_transaction_dates', Transaction.source_date, Transaction.local_date)
