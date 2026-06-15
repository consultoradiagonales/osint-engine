from __future__ import annotations

import json
from pathlib import Path

from .models import Radiografia


def write_reports(
    report: Radiografia,
    output_base: Path,
    *,
    write_json: bool = True,
    write_markdown: bool = True,
) -> list[Path]:
    output_base.parent.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    if write_json:
        json_path = output_base.with_suffix(".json")
        json_path.write_text(
            json.dumps(report.as_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        written.append(json_path)

    if write_markdown:
        markdown_path = output_base.with_suffix(".md")
        markdown_path.write_text(render_markdown(report), encoding="utf-8")
        written.append(markdown_path)

    return written


def render_markdown(report: Radiografia) -> str:
    lines = [
        f"# OSINT Radiografia: {report.target}",
        "",
        f"- Target type: {report.target_type}",
        f"- Generated at: {report.generated_at}",
        "",
        "## Key Findings",
    ]

    if report.findings:
        for finding in report.findings:
            lines.append(
                f"- **{finding.title}** ({finding.confidence}): {finding.detail}"
            )
    else:
        lines.append("- No findings were produced.")

    lines.extend(["", "## Source Table", ""])
    lines.append("| Claim | Value | Source | Confidence | URL | Collected At |")
    lines.append("|---|---|---|---|---|---|")
    for item in report.evidence:
        value = _cell(item.value)
        url = _cell(item.url or "")
        lines.append(
            f"| {_cell(item.claim)} | {value} | {_cell(item.source)} | "
            f"{item.confidence} | {url} | {item.collected_at} |"
        )

    if report.errors:
        lines.extend(["", "## Collector Notes", ""])
        for error in report.errors:
            lines.append(f"- {error}")

    lines.extend(
        [
            "",
            "## Caveats",
            "",
            "- Findings are leads unless independently verified.",
            "- Public source availability can change over time.",
            "- Use only for lawful, authorized and proportionate research.",
            "",
        ]
    )
    return "\n".join(lines)


def _cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()
