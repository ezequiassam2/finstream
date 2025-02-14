import logging
import re

from .strategies.parse_vss110 import ParseVSS110
from .strategies.parsing_strategy import ParsingStrategy


class ItemProcessor:
    def __init__(self):
        self.strategies = {
            'VSS-110': ParseVSS110(),
            # Adicionar outras strategies
        }

    def process(self, content):
        report_id = ParsingStrategy.get_report_id(content)
        logging.info(f"Processando relatório com o id: {report_id}")
        strategy = self.strategies.get(report_id)

        if strategy:
            return strategy.parse(content)
        else:
            logging.warning(f"Parse para {report_id} não encontrado")
            return None
