from core.strategies import register_strategy
from core.strategies.base_strategy import ParsingStrategy


@register_strategy("VSS-110")
class VSS110Strategy(ParsingStrategy):
    def parse_body(self, line: str, amounts: list, current_section: str) -> None:
        amounts.append(
            {
                "section": current_section,
                "label": line[0:25].strip(),
                "count": line[26:50].strip(),
                "credit_amount": line[51:75].strip(),
                "debit_amount": line[76:100].strip(),
                "total_amount": line[101:].strip()
            }
        )
