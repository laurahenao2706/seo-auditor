import unittest

from seo_auditor.application.serializers import report_to_csv, report_to_json


class SerializerTestCase(unittest.TestCase):
    def test_report_to_csv_has_header(self) -> None:
        rows = [
            {
                "rule_id": 1,
                "item": "Archivo robots.txt",
                "status": "PASS",
                "details": "ok",
                "recommendation": "none",
                "automated": True,
            }
        ]
        csv_payload = report_to_csv(rows)
        self.assertIn("rule_id,item,status,details,recommendation,automated", csv_payload)
        self.assertIn("Archivo robots.txt", csv_payload)

    def test_report_to_json_formats_pretty(self) -> None:
        payload = {"summary": {"PASS": 1}}
        json_payload = report_to_json(payload)
        self.assertIn("\n", json_payload)
        self.assertIn("\"PASS\": 1", json_payload)


if __name__ == "__main__":
    unittest.main()
