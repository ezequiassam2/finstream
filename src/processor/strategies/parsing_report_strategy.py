import logging
import re

from .convert_model import convert_amount


class ParsingStrategy:
    PATTERN_FORM = r"(?P<key>((\w+\s)?){1,2}\w+):\s+(?P<value>.+?)(?=\s{3,}|$)|(?:\s{3,})(?P<report_names>[\w\s]+)(?=\s{3,}|$)"
    PATTERN_SECTION = r'^[A-Z ]+$'
    PATTERN_DATA_LINE = r'[0-9]'
    PATTERN_FORM_DATA = r'(.*):(.*)'
    PATTERN_HEADER_TABLE = r"CREDIT\s+DEBIT\s+TOTAL|COUNT\s+AMOUNT\s+AMOUNT\s+AMOUNT"
    PATTERN_REPORT_ID = r'^\f?REPORT ID:  (VSS-\d+)'

    @staticmethod
    def get_report_id(content):
        match = re.match(ParsingStrategy.PATTERN_REPORT_ID, content)
        if match:
            return match.group(1)

    def strip(self, line):
        return line.strip()

    def is_empty_line(self, line):
        return not self.strip(line)

    def is_end_report(self, line):
        return "*** END OF VSS-110 REPORT ***" in self.strip(line)

    def is_no_data(self, line):
        return "*** NO DATA FOR THIS REPORT ***" in self.strip(line)

    def is_form_data(self, line):
        return re.match(self.PATTERN_FORM_DATA, line)

    def is_section_header(self, line):
        return re.match(self.PATTERN_SECTION, line)

    def is_data_line(self, line):
        return re.search(self.PATTERN_DATA_LINE, line)

    def parse_header_line(self, line, current_report):
        if "REPORT_HEADER" not in current_report:
            current_report["REPORT_HEADER"] = {}
        for match in re.finditer(self.PATTERN_FORM, line):
            if match.group('key'):
                current_report["REPORT_HEADER"].update({match.group("key").strip(): match.group("value").strip()})
            if match.group("report_names"):
                if "SUMMARY" not in current_report["REPORT_HEADER"]:
                    current_report["REPORT_HEADER"]["SUMMARY"] = []
                current_report["REPORT_HEADER"]["SUMMARY"].append(match.group("report_names").strip())
        return current_report

    def parse_content(self, content):
        raise NotImplementedError("parse_content não implementado")

    def parse(self, content):
        report_id = self.get_report_id(content)
        logging.info(f"Iniciando parse do {report_id}")
        parsed_content = self.parse_content(content)
        if not parsed_content:
            logging.info(f"Sem dados para {report_id}")
            return
        logging.info(f"Parse do {report_id} concluído")
        return convert_amount(parsed_content)
