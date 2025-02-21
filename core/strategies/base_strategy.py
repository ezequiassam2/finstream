import re
from abc import ABC, abstractmethod

from core.models.schemas import ReportSchema


class ParsingStrategy(ABC):
    HEADER_PATTERN = r"(.*?):\s*(.*?)(?=\s{2,}|$)"
    HEADER_FORM = r"(?P<key>((\w+\s)?){1,2}\w+):\s*(?P<value>.+?)(?=\s{3,}|$)|(?:\s{3,})(?P<summary>[\w\s]+)(?=\s{3,}|$)"
    SECTION_PATTERN = r"^\s?(\d{2}\-)?[A-Z\s]+$"

    @abstractmethod
    def parse_body(self, line: str, amounts: list, current_section: str) -> None:
        pass

    def parse_header(self, line: str, header: dict) -> None:
        for match in re.finditer(self.HEADER_FORM, line):
            if match.group('key'):
                header[match.group("key").strip().lower().replace(' ', '_')] = match.group("value").strip()
            if match.group("summary"):
                header.get('summary').append(match.group("summary").strip())

    def parse_section(self, current_section: str, line: str, previous_indent: int):
        current_indent = len(line) - len(line.lstrip())
        if current_indent > previous_indent:
            if current_section:
                current_section = f"{current_section} - {line.strip()}"
            else:
                current_section = line.strip()
            previous_indent = current_indent
        else:
            previous_indent = 0
            current_section = line.strip()
        return current_section, previous_indent

    def parse(self, content: str) -> ReportSchema:
        header, amounts, current_section, previous_indent = {'summary': []}, [], None, 0
        for line in content.strip().splitlines():
            if not line.strip():
                continue
            if '***' in line:
                break
            if re.match(self.HEADER_PATTERN, line):
                self.parse_header(line, header)
            elif re.match(self.SECTION_PATTERN, line):
                current_section, previous_indent = self.parse_section(current_section, line, previous_indent)
            elif any(c.isdigit() for c in line):
                self.parse_body(line, amounts, current_section)

        report = {**header, 'amounts': amounts}
        return ReportSchema(**report)
