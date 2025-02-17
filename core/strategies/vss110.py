import re

from core.models.schemas import ReportSchema
from core.strategies import register_strategy
from core.strategies.base_strategy import ParsingStrategy


@register_strategy("VSS-110")
class VSS110Strategy(ParsingStrategy):
    HEADER_PATTERN = r"^(.*?):\s{2,}(.*?)(?=\s{2,}|$)"
    HEADER_FORM = r"(?P<key>((\w+\s)?){1,2}\w+):\s+(?P<value>.+?)(?=\s{3,}|$)|(?:\s{3,})(?P<summary>[\w\s]+)(?=\s{3,}|$)"
    SECTION_PATTERN = r"^\f?[A-Z\s]+$"

    def parse(self, content: str) -> ReportSchema:
        header, amounts, current_section = {'summary': []}, [], None

        for line in content.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            if '***' in line:
                break
            if re.match(self.HEADER_PATTERN, line):
                for match in re.finditer(self.HEADER_FORM, line):
                    if match.group('key'):
                        header[match.group("key").strip().lower().replace(' ', '_')] = match.group("value").strip()
                    if match.group("summary"):
                        header.get('summary').append(match.group("summary").strip())
            elif re.match(self.SECTION_PATTERN, line):
                current_section = line
            elif current_section and any(c.isdigit() for c in line):
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

        report = {**header, 'amounts': amounts}
        return ReportSchema(**report)
