from __future__ import annotations

from ..models import Evidence


def collect_wayback(domain: str, timeout: float = 12.0, limit: int = 50) -> list[Evidence]:
    try:
        import requests
    except ImportError as exc:
        raise RuntimeError("requests is required for Wayback collection.") from exc

    api_url = (
        "https://web.archive.org/cdx"
        f"?url=*.{domain}/*"
        "&output=json"
        "&fl=timestamp,original,statuscode,mimetype,digest"
        "&filter=statuscode:200"
        "&collapse=urlkey"
        f"&limit={limit}"
    )
    response = requests.get(
        api_url,
        timeout=timeout,
        headers={"User-Agent": "ConsultoraDiagonalesOSINT/0.1"},
    )
    response.raise_for_status()
    rows = response.json()
    if not isinstance(rows, list) or len(rows) <= 1:
        return []

    headers = rows[0]
    evidence: list[Evidence] = []
    for row in rows[1:]:
        if not isinstance(row, list) or len(row) != len(headers):
            continue
        data = dict(zip(headers, row, strict=True))
        original = str(data.get("original", ""))
        timestamp = str(data.get("timestamp", ""))
        archive_url = f"https://web.archive.org/web/{timestamp}/{original}" if timestamp else None
        evidence.append(
            Evidence(
                source="wayback",
                claim="archived_url",
                value=original,
                url=archive_url,
                confidence="Medium",
                raw=data,
            )
        )
    return evidence
