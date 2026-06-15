from __future__ import annotations

from ..models import Evidence

RECORD_TYPES = ("A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME")


def collect_dns_records(domain: str, timeout: float = 12.0) -> list[Evidence]:
    try:
        import dns.exception
        import dns.resolver
    except ImportError as exc:
        raise RuntimeError("dnspython is required for DNS collection.") from exc

    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = timeout
    evidence: list[Evidence] = []

    for record_type in RECORD_TYPES:
        try:
            answers = resolver.resolve(domain, record_type, raise_on_no_answer=False)
        except (dns.resolver.NXDOMAIN, dns.resolver.NoNameservers, dns.exception.Timeout):
            continue
        except dns.resolver.NoAnswer:
            continue

        for answer in answers:
            value = answer.to_text().strip()
            evidence.append(
                Evidence(
                    source="dns",
                    claim=f"{record_type}_record",
                    value=value,
                    confidence="High",
                    raw={"record_type": record_type},
                )
            )

    return evidence
