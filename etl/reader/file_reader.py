import mmap
import re
from typing import Iterator, Dict, Any

import ijson

from core.utils.logger import get_logger

logger = get_logger(__name__)

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
        """Conta itens usando mmap."""
        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            try:
                for _ in ijson.items(mm, 'item'):
                    count += 1
            except ijson.common.JSONError as e:
                logger.info(f"Error parsing JSON at position {mm.tell()}: {e}")
            finally:
                mm.close()
        return count

    def read_txt(self, file_path: str) -> Iterator[Dict[str, Any]]:
        """Lê TXT sequencial, mas conta seções em paralelo."""
        def get_report_id(line: str) -> str:
            return re.match(self.pattern_report_id, line).group(1) if re.match(self.pattern_report_id, line) else None

        total = self._count_txt_sections_parallel(file_path)
        with open(file_path, 'r', encoding=self.encoding) as f:
            buffer = []
            section_num = 0
            for line in f:
                section_id = get_report_id(line)
                if section_id and buffer:
                        yield self._build_section(buffer, section_num, get_report_id(''.join(buffer)), total)
                        buffer = [line]
                        section_num += 1
                else:
                    buffer.append(line)
            yield self._build_section(buffer, section_num, get_report_id(''.join(buffer)), total)

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
