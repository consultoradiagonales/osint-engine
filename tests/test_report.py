import unittest

from osint_engine.models import Evidence, Radiografia
from osint_engine.report import render_markdown


class ReportTests(unittest.TestCase):
    def test_render_markdown_includes_evidence(self):
        report = Radiografia(target="example.com", target_type="domain")
        report.evidence.append(
            Evidence(
                source="manual-query",
                claim="google",
                value="review",
                url="https://example.com",
            )
        )

        markdown = render_markdown(report)

        self.assertIn("# OSINT Radiografia: example.com", markdown)
        self.assertIn("| google | review | manual-query |", markdown)


if __name__ == "__main__":
    unittest.main()
