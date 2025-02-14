import json
import re

from ..processor.strategies.parsing_report_strategy import ParsingStrategy


class ItemReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_type = file_path.split('.')[-1].lower()

    def read(self):
        if self.file_type == 'txt':
            return self._read_txt()
        elif self.file_type == 'json':
            return self._read_json()
        else:
            raise ValueError(f"Leitor não encontrado para o tipo de arquivo: {self.file_type}")

    def _read_txt(self):
        section_buffer = []
        with open(self.file_path, 'r') as file:
            for line in file:
                if re.match(ParsingStrategy.PATTERN_REPORT_ID, line):
                    yield ''.join(section_buffer)
                    section_buffer = []
                section_buffer.append(line)
            if section_buffer:
                yield ''.join(section_buffer)

    def _read_json(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)