import unittest

from osint_engine.engine import EngineOptions, run_domain_radiografia


class EngineTests(unittest.TestCase):
    def test_offline_run_generates_manual_queries(self):
        report = run_domain_radiografia("example.com", EngineOptions(offline=True))

        self.assertEqual(report.target, "example.com")
        self.assertEqual(report.errors, [])
        self.assertTrue(any(item.source == "manual-query" for item in report.evidence))
        self.assertTrue(
            any(finding.title == "Manual review queries prepared" for finding in report.findings)
        )


if __name__ == "__main__":
    unittest.main()
