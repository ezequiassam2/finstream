from typing import Iterator

import ijson

from core.utils.utils import get_report_id


class FileReader:
    def __init__(self, encoding: str = 'utf-8'):
        self.encoding = encoding

    def read_json(self, file_path) -> Iterator[dict]:
        total = self.__count_json_items(file_path)
        with open(file_path, 'r', encoding=self.encoding) as f:
            section_num = 0
            for record in ijson.items(f, 'item'):  # Stream de objetos JSON
                yield {"raw": record, "section_num": section_num, "section_id": record.get("arn", 0), "total": total}

    def read_txt(self, file_path) -> Iterator[dict]:
        total = self.__count_txt_sections(file_path)
        with open(file_path, 'r', encoding=self.encoding) as f:
            buffer = []
            section_num = 0
            for line in f:
                report_id = get_report_id(line)
                if report_id:
                    if buffer:
                        yield {"raw": ''.join(buffer), "section_num": section_num, "section_id": report_id,
                               "total": total}
                        section_num += 1
                    buffer = [line]
                else:
                    buffer.append(line)
            yield {"raw": ''.join(buffer), "section_num": section_num, "section_id": get_report_id(''.join(buffer)),
                   "total": total}

    def __count_json_items(self, file_path) -> int:
        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            for _ in ijson.items(f, 'item'):
                count += 1
        return count

    def __count_txt_sections(self, file_path) -> int:
        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if get_report_id(line):
                    count += 1
        return count