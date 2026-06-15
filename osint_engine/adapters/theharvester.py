from __future__ import annotations

from .external_cli import run_external
from ..models import Evidence


def collect_theharvester(domain: str, timeout: float = 60.0, limit: int = 50) -> list[Evidence]:
    output = run_external(
        ["theHarvester", "-d", domain, "-b", "duckduckgo,bing"],
        timeout=timeout,
    )
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    evidence: list[Evidence] = []
    for line in lines[:limit]:
        evidence.append(
            Evidence(
                source="theHarvester",
                claim="cli_output",
                value=line[:500],
                confidence="Low",
                raw={"note": "Raw CLI output. Review manually before using as fact."},
            )
        )
    return evidence
