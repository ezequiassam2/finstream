import re

from core.strategies import register_strategy
from core.strategies.base_strategy import ParsingStrategy


@register_strategy("VSS-600")
class VSS110Strategy(ParsingStrategy): #todo: mudar a forma como captura o nome da seção, fazer logica de linha anterior, fazer validação para não salvar cabeçalho da tabelha em section, identificar tabulação de não numericos
    def parse_body(self, line: str, amounts: list, current_section: str) -> None:
        parts = re.split(r'\s{2,}', line.strip())
        if len(parts) <= 1:
            return
        while len(parts) < 7:
            parts.insert(1, None)
        amounts.append(
            {
                "section": current_section,
                "label": self.get_part(parts, 0),
                "processing_date": self.get_part(parts, 1),
                "processing_count": self.get_part(parts, 2),
                "transaction_amount": self.get_part(parts, 3),
                "interchange_fee": self.get_part(parts, 4),
                "processing_charge": self.get_part(parts, 5),
                "settlement_amount": self.get_part(parts, 6)
            })

    def get_part(self, parts, index):
        return parts[index].strip() if parts[index] else None
