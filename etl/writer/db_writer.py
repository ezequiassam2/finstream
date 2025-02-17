from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models.database import Report, Amount, Base
from core.utils.logger import get_logger

logger = get_logger(__name__)

class DBWriter:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_report(self, data: dict):
        session = self.Session()
        try:
            report = Report(**{k: v for k, v in data.items() if k != 'amounts'})
            session.add(report)
            session.flush()

            amounts = [Amount(report_id=report.id, **amount) for amount in data['amounts']]
            session.bulk_save_objects(amounts)
            session.commit()
        except Exception as e:
            logger.error(f"Erro ao salvar: {e}")
            session.rollback()
            raise
        finally:
            session.close()
