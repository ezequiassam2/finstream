from datetime import datetime
from decimal import Decimal

from src.writer.model import Amounts


def convert_amount(parsed_content):
    report_header = parsed_content.get("REPORT_HEADER", {})
    base_amount_dict = {
        "report_id": report_header.get("REPORT ID"),
        "summary": ", ".join(report_header.get("SUMMARY", [])),
        "page": int(report_header.get("PAGE", 0)),
        "report_for": report_header.get("REPORTING FOR"),
        "proc_date": __to_date(report_header.get("PROC DATE")),
        "rollup_to": report_header.get("ROLLUP TO"),
        "report_date": __to_date(report_header.get("REPORT DATE")),
        "funds_xfer_entity": report_header.get("FUNDS XFER ENTITY"),
        "settlement_currency": report_header.get("SETTLEMENT CURRENCY")
    }

    amounts_list = []

    for section, values in parsed_content.items():
        if section == "REPORT_HEADER":
            if len(parsed_content) == 1:
                amounts_list.append(Amounts(**base_amount_dict))
            continue
        for value in values:
            amount_data = base_amount_dict.copy()
            amount_data.update({
                "section": section,
                "label": value.get("label"),
                "count": __to_decimal("count", value),
                "credit_amount": __to_decimal("credit_amount", value),
                "debit_amount": __to_decimal("debit_amount", value),
                "total_amount": __to_decimal("total_amount", value)
            })
            amounts_list.append(Amounts(**amount_data))
    return amounts_list


def __to_date(date_str):
    return datetime.strptime(date_str, '%d%b%y').isoformat() if date_str else date_str


def __to_decimal(key, value):
    v = value.get(key, "") if key in value else ""
    if not v:
        return Decimal(0)
    is_debit = v.endswith("DB")
    v = v.replace(",", "").replace("DB", "").replace("CR", "")
    return -Decimal(v) if is_debit else Decimal(v)
