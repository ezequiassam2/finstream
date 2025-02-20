from typing import Iterator

import ijson

from core.utils.utils import get_report_id


class FileReader:
    def __init__(self, encoding: str = 'utf-8'):
        self.encoding = encoding

    def read_json(self, file_path) -> Iterator[dict]:
        total = self.__count_json_items(file_path)
        with open(file_path, 'r', encoding=self.encoding) as f:
            for record in ijson.items(f, 'item'):  # Stream de objetos JSON
                yield record, total

    def read_txt(self, file_path) -> Iterator[str]:
        total = self.__count_txt_sections(file_path)
        with open(file_path, 'r', encoding=self.encoding) as f:
            buffer = []
            for line in f:
                if get_report_id(line):
                    if buffer:
                        yield ''.join(buffer), total
                    buffer = [line]
                else:
                    buffer.append(line)
            yield ''.join(buffer), total

    def __count_json_items(file_path: str) -> int:
        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            for _ in ijson.items(f, 'item'):
                count += 1
        return count

    def __count_txt_sections(file_path: str) -> int:
        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if get_report_id(line):
                    count += 1
        return count