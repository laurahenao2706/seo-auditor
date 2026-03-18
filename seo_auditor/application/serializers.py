from __future__ import annotations

import csv
import io
import json
from typing import Any


def report_to_csv(rows: list[dict[str, Any]]) -> str:
    output = io.StringIO()
    fieldnames = ["rule_id", "item", "status", "details", "recommendation", "automated"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def report_to_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)
