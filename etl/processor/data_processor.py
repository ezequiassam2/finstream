from core.models.schemas import TransactionSchema
from core.strategies import StrategyFactory
from core.strategies import vss110, vss115, vss120, vss130, vss135, vss140, vss210, vss215, vss230, vss300, vss600, \
    vss610, vss900, vss910, vss930  # noqa importando parsers
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
            data = TransactionSchema(**content).model_dump()
            data.update({"line_segment": section_count, "content_raw": content})
            return data
        except Exception as e:
            logger.error(f"[Transação] Erro ao processar segmento={section_count} para o mcc={mcc} -  {str(e)}")
            raise
