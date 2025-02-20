from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models.database import Report, Amount, Base, Transaction
from core.utils.logger import get_logger

logger = get_logger(__name__)

class DBWriter:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_report(self, data: dict):
        session = self.Session()
        report_id = data.get("report_id")
        try:
            report = Report(**{k: v for k, v in data.items() if k != 'amounts'})
            session.add(report)
            session.flush()

            amounts = [Amount(report_id=report.id, **amount) for amount in data['amounts']]
            session.bulk_save_objects(amounts)
            session.commit()
            logger.info(f"Relatorio {report_id} salvo com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao salvar relatorio {report_id}: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def save_transaction(self, data: dict):
        session = self.Session()
        arn = data.get("arn")
        try:
            transaction = Transaction(**data)
            session.add(transaction)
            session.commit()
            logger.info(f"Transação {arn} salva com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao salvar transação {arn}: {e}")
            session.rollback()
            raise
        finally:
            session.close()