from typing import Iterator

import ijson

from core.utils.utils import get_report_id


class FileReader:
    def __init__(self, encoding: str = 'utf-8'):
        self.encoding = encoding

    def read_json(self, file_path) -> Iterator[dict]:
        with open(file_path, 'r', encoding=self.encoding) as f:
            for record in ijson.items(f, 'item'):  # Stream de objetos JSON
                yield record

    def read_txt(self, file_path) -> Iterator[str]:
        with open(file_path, 'r', encoding=self.encoding) as f:
            buffer = []
            for line in f:
                if get_report_id(line):
                    if buffer:
                        yield ''.join(buffer)
                    buffer = [line]
                else:
                    buffer.append(line)
            yield ''.join(buffer)
