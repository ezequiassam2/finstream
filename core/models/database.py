
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, JSON, Index, func
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

Index('ix_report_section', Amount.section)
Index('ix_report_date_currency', Report.report_date, Report.settlement_currency)
