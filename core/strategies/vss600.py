import re

from core.strategies import register_strategy
from core.strategies.base_strategy import ParsingStrategy


@register_strategy("VSS-600")
class VSS600Strategy(ParsingStrategy):
    def parse_body(self, line: str, amounts: list, current_section: str, line_index: int) -> None:
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
                "settlement_amount": self.get_part(parts, 6),
                "index": line_index
            })

    def get_part(self, parts, index):
        return parts[index].strip() if parts[index] else None
