from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .adapters.theharvester import collect_theharvester
from .collectors.certificate_transparency import collect_crtsh
from .collectors.dns_records import collect_dns_records
from .collectors.http_probe import collect_http_probe
from .collectors.manual_queries import collect_manual_queries
from .collectors.wayback import collect_wayback
from .models import Evidence, Finding, Radiografia
from .safety import normalize_domain

Collector = Callable[[str], list[Evidence]]


@dataclass(slots=True)
class EngineOptions:
    offline: bool = False
    include_theharvester: bool = False
    timeout: float = 12.0
    limit: int = 50


def run_domain_radiografia(target: str, options: EngineOptions | None = None) -> Radiografia:
    opts = options or EngineOptions()
    domain = normalize_domain(target)
    report = Radiografia(target=domain, target_type="domain")

    collectors: list[tuple[str, Collector]] = [("manual_queries", collect_manual_queries)]
    if not opts.offline:
        collectors.extend(
            [
                ("dns_records", lambda value: collect_dns_records(value, timeout=opts.timeout)),
                ("http_probe", lambda value: collect_http_probe(value, timeout=opts.timeout)),
                ("crtsh", lambda value: collect_crtsh(value, timeout=opts.timeout, limit=opts.limit)),
                ("wayback", lambda value: collect_wayback(value, timeout=opts.timeout, limit=opts.limit)),
            ]
        )

    if opts.include_theharvester:
        collectors.append(
            (
                "theharvester",
                lambda value: collect_theharvester(value, timeout=opts.timeout, limit=opts.limit),
            )
        )

    for name, collector in collectors:
        try:
            report.evidence.extend(collector(domain))
        except Exception as exc:  # noqa: BLE001 - failures must not kill a full OSINT run.
            report.errors.append(f"{name}: {exc}")

    report.findings = build_findings(report.evidence)
    return report


def build_findings(evidence: list[Evidence]) -> list[Finding]:
    findings: list[Finding] = []

    dns_values = [item for item in evidence if item.source == "dns"]
    if dns_values:
        findings.append(
            Finding(
                title="DNS footprint detected",
                detail=f"{len(dns_values)} public DNS records were collected.",
                confidence="High",
                evidence_sources=["dns"],
            )
        )

    cert_hosts = {
        item.value
        for item in evidence
        if item.source == "crt.sh" and item.claim == "certificate_name"
    }
    if cert_hosts:
        findings.append(
            Finding(
                title="Certificate transparency hosts found",
                detail=f"{len(cert_hosts)} unique names appeared in public certificate logs.",
                confidence="Medium",
                evidence_sources=["crt.sh"],
            )
        )

    wayback_urls = [item for item in evidence if item.source == "wayback"]
    if wayback_urls:
        findings.append(
            Finding(
                title="Historical URLs available",
                detail=f"{len(wayback_urls)} archived URLs were found in Wayback Machine.",
                confidence="Medium",
                evidence_sources=["wayback"],
            )
        )

    manual_queries = [item for item in evidence if item.source == "manual-query"]
    if manual_queries:
        findings.append(
            Finding(
                title="Manual review queries prepared",
                detail=f"{len(manual_queries)} search URLs are ready for analyst review.",
                confidence="High",
                evidence_sources=["manual-query"],
            )
        )

    return findings
