import json
import re

from src.processor.strategies.parsing_strategy import ParsingStrategy


class ItemReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        pass

class TxtReader(ItemReader):
    def read(self):
        section_buffer = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if re.match(ParsingStrategy.PATTERN_REPORT_ID, line) and section_buffer:
                    yield ''.join(section_buffer)
                    section_buffer = []
                section_buffer.append(line)
            if section_buffer:
                yield ''.join(section_buffer)

class JsonReader(ItemReader):
    def read(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)