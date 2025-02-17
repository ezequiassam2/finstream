from core.strategies import StrategyFactory
from core.strategies import vss110  # noqa importando parsers
from core.utils.logger import get_logger
from core.utils.utils import get_report_id

logger = get_logger(__name__)


class DataProcessor:
    def process(self, content: str, section_count: int) -> dict:
        report_id = get_report_id(content)
        strategy_class = StrategyFactory.get_strategy(report_id)
        if not strategy_class:
            logger.error(f"Parse não encontrado para {report_id}")
            return {}
        try:
            strategy = strategy_class()
            logger.info(f"Processando segmento={section_count} do report_id={report_id}")
            data = strategy.parse(content).model_dump()
            data.update({"file_segment": section_count, "content_raw": content})
            return data
        except Exception as e:
            logger.error(f"Erro ao processar segmento={section_count} para o report_id={report_id} -  {str(e)}")
            raise
