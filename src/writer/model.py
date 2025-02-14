from sqlalchemy import Column, Integer, String, DateTime, DECIMAL
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ModelRepository(Base):
    __abstract__ = True
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Amounts(ModelRepository):
    __tablename__ = 'amounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(String, nullable=False)
    summary = Column(String)
    page = Column(Integer)
    report_for = Column(String)
    proc_date = Column(DateTime)
    rollup_to = Column(String)
    report_date = Column(DateTime)
    funds_xfer_entity = Column(String)
    settlement_currency = Column(String)
    section = Column(String)
    label = Column(String)
    count = Column(DECIMAL)
    credit_amount = Column(DECIMAL)
    debit_amount = Column(DECIMAL)
    total_amount = Column(DECIMAL)


class Transactions(ModelRepository):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String)
    count = Column(Integer)
    credit_amount = Column(DECIMAL)
    debit_amount = Column(DECIMAL)
    total_amount = Column(DECIMAL)
