from __future__ import annotations

from ..models import Evidence


def collect_crtsh(domain: str, timeout: float = 12.0, limit: int = 50) -> list[Evidence]:
    try:
        import requests
    except ImportError as exc:
        raise RuntimeError("requests is required for crt.sh collection.") from exc

    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "ConsultoraDiagonalesOSINT/0.1"},
    )
    response.raise_for_status()
    rows = response.json()
    if not isinstance(rows, list):
        return []

    evidence: list[Evidence] = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        name_value = str(row.get("name_value", ""))
        for name in name_value.splitlines():
            clean_name = name.strip().lower().lstrip("*.").strip(".")
            if not clean_name or clean_name in seen:
                continue
            if not clean_name.endswith(domain):
                continue
            seen.add(clean_name)
            evidence.append(
                Evidence(
                    source="crt.sh",
                    claim="certificate_name",
                    value=clean_name,
                    url=url,
                    confidence="Medium",
                    raw={
                        "issuer_name": row.get("issuer_name"),
                        "entry_timestamp": row.get("entry_timestamp"),
                    },
                )
            )
            if len(evidence) >= limit:
                return evidence

    return evidence
