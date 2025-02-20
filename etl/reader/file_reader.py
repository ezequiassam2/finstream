import mmap
import os
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Iterator, Dict, Any

import ijson


class FileReader:
    def __init__(self, encoding: str = 'utf-8'):
        self.encoding = encoding
        self.pattern_report_id = r"^\f?REPORT ID:\s+(VSS-\d+)"

    def read_json(self, file_path: str) -> Iterator[Dict[str, Any]]:
        """Lê JSON de forma sequencial, mas conta itens em paralelo."""
        total = self._count_json_items_parallel(file_path)
        with open(file_path, 'r', encoding=self.encoding) as f:
            for section_num, record in enumerate(ijson.items(f, 'item')):
                yield {
                    "raw": record,
                    "section_num": section_num,
                    "section_id": record.get("arn", section_num),
                    "total": total
                }

    def _count_json_items_parallel(self, file_path: str) -> int:
        """Conta itens em paralelo."""
        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            items = ijson.items(f, 'item')
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(lambda: 1) for _ in items]
                count = sum(f.result() for f in futures)
        return count

    def read_txt(self, file_path: str) -> Iterator[Dict[str, Any]]:
        """Lê TXT sequencial, mas conta seções em paralelo."""
        total = self._count_txt_sections_parallel(file_path)
        with open(file_path, 'r', encoding=self.encoding) as f:
            buffer = []
            section_num = 0
            for line in f:
                section_id = re.match(self.pattern_report_id, line).group(1) if re.match(self.pattern_report_id, line) else None
                if section_id:
                    if buffer:
                        yield self._build_section(buffer, section_num, section_id, total)
                        buffer = [line]
                        section_num += 1
                else:
                    buffer.append(line)
            yield self._build_section(buffer, section_num, section_id if section_id else re.match(self.pattern_report_id, ''.join(buffer)).group(1), total)

    def _count_txt_sections_parallel(self, file_path: str) -> int:
        """Conta seções em paralelo usando mmap."""
        start_regex = re.compile(self.pattern_report_id.encode(), re.MULTILINE)
        with open(file_path, 'r', encoding=self.encoding) as f:
                mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                total = len(start_regex.findall(mm))
                mm.close()
                return total

    def _build_section(self, buffer: list, section_num: int, section_id: str, total: int) -> Dict[str, Any]:
        return {
            "raw": ''.join(buffer),
            "section_num": section_num,
            "section_id": section_id,
            "total": total
        }
