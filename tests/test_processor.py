import json
import os

from etl.processor.data_processor import DataProcessor

def read_file_content(file_name):
    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, f"resources/{file_name}"), 'r') as file:
        return file.read()

def test_process_report():
    processor = DataProcessor()
    raw_content = read_file_content("raw_vss110.txt")
    content = {
        "section_id": "VSS-110",
        "section_num": 1,
        "raw": raw_content
    }
    result = processor.process_report(content)
    assert result['report_id'] == "VSS-110"
    assert result['amounts'][0]['data']['total_amount'] == -28081919.39


def test_process_transaction():
    processor = DataProcessor()
    raw_content = read_file_content("raw_clearing.json")
    content = {
        "section_id": "123456",
        "section_num": 1,
        "raw": json.loads(raw_content)[0]
    }
    result = processor.process_transaction(content)
    assert result['arn'] == '33478'
    assert result['purchase_value'] == 21.0
