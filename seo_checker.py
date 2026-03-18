from __future__ import annotations

import argparse
import json
from typing import Any

from seo_auditor.application.serializers import report_to_csv, report_to_json
from seo_auditor.application.service import SeoAuditService
from seo_auditor.infrastructure.http_client import RequestsHttpClient


class SEOChecker:
    """Facade de compatibilidad para preservar la API publica previa."""

    def __init__(self, timeout: int = 12, sample_size: int = 25) -> None:
        self.service = SeoAuditService(http_client=RequestsHttpClient(timeout=timeout), sample_size=sample_size)

    def analyze(self, input_url: str) -> dict[str, Any]:
        return self.service.analyze(input_url)


def run_cli() -> None:
    parser = argparse.ArgumentParser(description="Validador SEO tecnico basado en checklist")
    parser.add_argument("url", help="URL a auditar")
    parser.add_argument("--out-json", help="Ruta para guardar el reporte JSON")
    parser.add_argument("--out-csv", help="Ruta para guardar el reporte CSV")
    args = parser.parse_args()

    checker = SEOChecker()
    result = checker.analyze(args.url)

    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))

    if args.out_json:
        with open(args.out_json, "w", encoding="utf-8") as file:
            file.write(report_to_json(result))

    if args.out_csv:
        with open(args.out_csv, "w", encoding="utf-8", newline="") as file:
            file.write(report_to_csv(result["results"]))


if __name__ == "__main__":
    run_cli()
