import re

from core.strategies import register_strategy
from core.strategies.base_strategy import ParsingStrategy


@register_strategy("VSS-600")
class VSS600Strategy(ParsingStrategy):
    def parse_section(self, current_section:str, line:str, previous_indent:int):
        if re.match(r"(\s+[A-Z]+\s+){5}", line):
            return current_section, previous_indent
        current_indent = len(line) - len(line.lstrip())
        if current_indent > previous_indent:
            if current_section:
                current_section = f"{current_section} - {line.strip()}"
            else:
                current_section = line.strip()
            previous_indent = current_indent
        elif current_indent  != 0 and current_indent == previous_indent:
            split = current_section.split(' - ')
            if len(split) > 2:
                current_section = f"{''.join(split[:len(split) - 1])} - {line.strip()}"
            else:
                current_section = f"{split[0]} - {line.strip()}"
        else:
            previous_indent = 0
            current_section = line.strip()
        return current_section, previous_indent

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
