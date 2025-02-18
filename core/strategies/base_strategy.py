import re
from abc import ABC, abstractmethod

from core.models.schemas import ReportSchema


class ParsingStrategy(ABC):
    HEADER_PATTERN = r"(.*?):\s*(.*?)(?=\s{2,}|$)"
    HEADER_FORM = r"(?P<key>((\w+\s)?){1,2}\w+):\s*(?P<value>.+?)(?=\s{3,}|$)|(?:\s{3,})(?P<summary>[\w\s]+)(?=\s{3,}|$)"
    SECTION_PATTERN = r"^\f?[A-Z\s]+$"

    @abstractmethod
    def parse_body(self, line: str, amounts: list, current_section: str) -> None:
        pass

    def parse_header(self, line: str, header: dict) -> None:
        for match in re.finditer(self.HEADER_FORM, line):
            if match.group('key'):
                header[match.group("key").strip().lower().replace(' ', '_')] = match.group("value").strip()
            if match.group("summary"):
                header.get('summary').append(match.group("summary").strip())

    def parse(self, content: str) -> ReportSchema:
        header, amounts, current_section = {'summary': []}, [], None

        for line in content.strip().splitlines():
            if not line.strip():
                continue
            if '***' in line:
                break
            if re.match(self.HEADER_PATTERN, line):
                self.parse_header(line, header)
                current_section = line.strip()
            elif re.match(self.SECTION_PATTERN, line):
                current_section = line.strip()
            elif current_section and any(c.isdigit() for c in line):
                self.parse_body(line, amounts, current_section)

        report = {**header, 'amounts': amounts}
        return ReportSchema(**report)
