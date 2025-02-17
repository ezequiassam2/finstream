import re

PATTERN_REPORT_ID = r'^\f?REPORT ID:  (VSS-\d+)'


def get_report_id(content):
    match = re.match(PATTERN_REPORT_ID, content)
    if match:
        return match.group(1)
