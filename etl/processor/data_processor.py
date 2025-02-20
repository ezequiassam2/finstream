from core.models.schemas import TransactionSchema
from core.strategies import StrategyFactory
from core.utils.logger import get_logger
from core.utils.utils import get_report_id

logger = get_logger(__name__)


class DataProcessor:
    def process_report(self, content: str, section_count: int) -> dict:
        report_id = get_report_id(content)
        strategy_class = StrategyFactory.get_strategy(report_id)
        if not strategy_class:
            logger.error(f"[Relatorio] Parse não encontrado para {report_id}")
            return {}
        try:
            strategy = strategy_class()
            logger.info(f"[Relatorio] Processando segmento={section_count} do report_id={report_id}")
            data = strategy.parse(content).model_dump()
            data.update({"file_segment": section_count, "content_raw": content})
            return data
        except Exception as e:
            logger.error(
                f"[Relatorio] Erro ao processar segmento={section_count} para o report_id={report_id} -  {str(e)}")
            raise

    def process_transaction(self, content: dict, section_count: int) -> dict:
        mcc = content.get("mcc")
        try:
            logger.info(f"[Transação] Processando linha segmento={section_count} para o mcc={mcc}")
            content.update({"line_segment": section_count, "content_raw": content.copy()})
            data = TransactionSchema(**content).model_dump()
            return data
        except Exception as e:
            logger.error(f"[Transação] Erro ao processar segmento={section_count} para o mcc={mcc} -  {str(e)}")
            raise
