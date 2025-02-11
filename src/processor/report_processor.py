import logging
from turtle import pd

from src.processor.strategies.parse_vss110 import ParseVSS110


class ReportProcessor:
    def __init__(self):
        self.strategies = {
            'VSS-110': ParseVSS110(),
            # Adicionar outras strategies
        }

    def process(self, section):
        report_id = self.extract_report_id(section)
        strategy = self.strategies.get(report_id)

        if strategy:
            return strategy.parse(section)
        else:
            logging.warning(f"Parse para {report_id} não encontrada. Usando padrão.")
            return pd.DataFrame()  # Retorna um DataFrame vazio ou log, ajustar conforme necessário

    def extract_report_id(self, section):
        lines = section.split('\n')
        for line in lines:
            if "REPORT ID:" in line:
                return line.split(':')[1].strip()
        return "default"
