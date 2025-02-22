import re

from core.strategies.base_strategy import ParsingStrategy


class GenericStrategy(ParsingStrategy):
    def __init__(self, index_insert=0, index_insert_last=False,
                 labels=['count', 'credit_amount', 'debit_amount', 'total_amount']):
        self.labels = labels
        self.len_columns = len(labels)
        self.last_index = index_insert_last
        self.index_insert = index_insert

    def parse_body(self, line: str, amounts: list, current_section: str, line_index: int) -> None:
        parts = re.split(r'\s{2,}', line.strip())
        label_section = parts.pop(0).strip() if parts else None
        while len(parts) < self.len_columns:
            if (self.last_index):
                parts.append(None)
            else:
                parts.insert(self.index_insert, None)

        data_parsed = {}
        for i, label in enumerate(self.labels):
            if parts[i]:
                data_parsed[label.lower()] = parts[i].strip()

        amounts.append({"section": current_section, "label": label_section, "data": data_parsed, "index": line_index})

    def parse_header(self, line: str, header: dict) -> None:
        super().parse_header(line, header)
        if 'clearing_currency' in header:
            header['settlement_currency'] = header.pop('clearing_currency')[:3]
