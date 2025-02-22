from core.models.schemas import TransactionSchema
from core.strategies import StrategyFactory
from core.strategies import vss110, vss115, vss120, vss130, vss135, vss140, vss210, vss215, vss230, vss300, vss600, \
    vss610, vss900, vss910, vss930  # noqa
from core.utils.logger import get_logger

logger = get_logger(__name__)


class DataProcessor:
    def process_report(self, content: dict) -> dict:
        report_id = content.get("section_id")
        section_num = content.get("section_num")
        content_raw = content.get("raw")
        strategy_class = StrategyFactory.get_strategy(report_id)
        if not strategy_class:
            logger.error(f"[Relatorio] Parse não encontrado para {report_id} segmento={section_num}")
            return {}
        try:
            strategy = strategy_class()
            logger.info(f"[Relatorio] Processando segmento={section_num} do report_id={report_id}")
            data = strategy.parse(content_raw).model_dump(exclude_none=True)
            data.update({"section_num": section_num, "raw": content_raw})
            return data
        except Exception as e:
            logger.error(
                f"[Relatorio] Erro ao processar segmento={section_num} para o report_id={report_id} -  {str(e)}")
            raise

    def process_transaction(self, content: dict) -> dict:
        arn = content.get("section_id")
        section_num = content.get("section_num")
        try:
            logger.info(f"[Transação] Processando linha segmento={section_num} para o section_id={arn}")
            data = TransactionSchema(**content.get("raw"), **content).model_dump()
            return data
        except Exception as e:
            logger.error(f"[Transação] Erro ao processar segmento={section_num} para o section_id={arn} -  {str(e)}")
            raise

    def process_last_section(self, report_old):
        strategy_class = StrategyFactory.get_strategy(report_old.report_id)
        strategy = strategy_class()
        return strategy.parser_last_section(report_old.raw)
