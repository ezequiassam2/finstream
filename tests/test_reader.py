import pytest
from etl.reader.file_reader import FileReader

def test_file_reader():
    reader = FileReader()
    content = reader.read("tests/sample.VSS-110.txt")
    assert "REPORT ID" in content
