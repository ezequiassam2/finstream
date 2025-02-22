from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload

from core.models.database import Report, Amount, Base, Transaction
from core.utils.logger import get_logger
from core.utils.utils import classify_transaction

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

    def get_report(self, report_id, reporting_for, page):
        session = self.Session()
        try:
            report = (session.query(Report)
                      .filter(Report.report_id == report_id)
                      .filter(Report.reporting_for == reporting_for)
                      .filter(Report.page == page)
                      .first())
            return report
        except Exception as e:
            logger.error(f"Erro ao buscar relatorio {report_id}: {e}")
            raise
        finally:
            session.close()

    def get_amounts_with_null_section(self, start_time):
        session = self.Session()
        try:
            query = (session.query(Amount)
                     .join(Report, Report.id == Amount.report_id)
                     .options(joinedload(Amount.report))
                     .filter(Amount.section == None)
                     .filter(Amount.created_at >= start_time)
                     .order_by(Report.reporting_for, Report.page, Amount.index))
            results = query.all()
            return results
        except Exception as e:
            logger.error(f"Erro ao executar a consulta: {e}")
            raise
        finally:
            session.close()

    def update_section(self, amount_id, section):
        session = self.Session()
        try:
            amount = session.query(Amount).filter(Amount.id == amount_id).one()
            amount.section = section
            session.commit()
            logger.info(f"Seção atualizada para {section} para o amount_id {amount_id}")
        except Exception as e:
            logger.error(f"Erro ao atualizar a seção para o amount_id {amount_id}: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    def update_transaction_class(self):
        session = self.Session()
        try:
            amounts = (session.query(Amount)
                       .join(Report, Report.id == Amount.report_id)
                       .filter(Amount.transaction_class == None)
                      .filter(Report.report_id == "VSS-600")
                       .all())
            for amount in amounts:
                split = amount.section.split(' - ')
                ep  = f"{split[1]} {amount.label}" if len(split) > 1 else  f"{amount.section} {amount.label}"
                transaction_class = classify_transaction(ep)
                if transaction_class:
                    amount.transaction_class = transaction_class
            session.commit()
            logger.info(f"Atualização do transaction_class executada para {len(amounts)} registros")
        except Exception as e:
            logger.error(f"Erro ao atualizar transaction_class: {e}")
            session.rollback()
            raise
        finally:
            session.close()
