import re

from ..parsing_report_strategy import ParsingStrategy


class ParseVSS110(ParsingStrategy):
    PATTERN_HEADER_TABLE = r"CREDIT\s+DEBIT\s+TOTAL|COUNT\s+AMOUNT\s+AMOUNT\s+AMOUNT"

    def parse_content(self, content):
        lines = content.strip().splitlines()
        current_section = None
        current_report = {}

        for line in lines:
            line = self.strip(line)
            if self.is_empty_line(line) or self.is_end_report(line) or self.is_header_table(line):
                continue

            if self.is_no_data(line):
                return current_report

            if self.is_form_data(line):
                self.parse_header_line(line, current_report)
                continue

            if self.is_section_header(line):
                current_section = line
                current_report[current_section] = []
                continue

            if current_section and self.is_data_line(line):
                report_entry = self.parse_data_line(line)
                current_report[current_section].append(report_entry)

        return current_report

    def is_header_table(self, line):
        return re.match(self.PATTERN_HEADER_TABLE, line)

    def parse_data_line(self, line):
        label = line[0:26].strip()
        count = line[25:49].strip()
        credit_amount = line[49:75].strip()
        debit_amount = line[75:100].strip()
        total_amount = line[100:].strip()

        return {
            "label": label or None,
            "count": count or None,
            "credit_amount": credit_amount or None,
            "debit_amount": debit_amount or None,
            "total_amount": total_amount or None
        }
