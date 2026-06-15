from __future__ import annotations

import re

from ..models import Evidence

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def collect_http_probe(domain: str, timeout: float = 12.0) -> list[Evidence]:
    try:
        import requests
    except ImportError as exc:
        raise RuntimeError("requests is required for HTTP probing.") from exc

    evidence: list[Evidence] = []
    for scheme in ("https", "http"):
        url = f"{scheme}://{domain}"
        try:
            response = requests.get(
                url,
                timeout=timeout,
                allow_redirects=True,
                headers={"User-Agent": "ConsultoraDiagonalesOSINT/0.1"},
            )
        except requests.RequestException:
            continue

        final_url = response.url
        evidence.append(
            Evidence(
                source="http",
                claim=f"{scheme}_status",
                value=str(response.status_code),
                url=final_url,
                confidence="High",
                raw={"headers": dict(_selected_headers(response.headers))},
            )
        )

        title = extract_title(response.text)
        if title:
            evidence.append(
                Evidence(
                    source="http",
                    claim=f"{scheme}_title",
                    value=title,
                    url=final_url,
                    confidence="Medium",
                )
            )

    return evidence


def extract_title(html: str) -> str | None:
    match = TITLE_RE.search(html[:200_000])
    if not match:
        return None
    return " ".join(match.group(1).split())[:240]


def _selected_headers(headers) -> dict[str, str]:
    names = ("server", "content-type", "location", "x-powered-by")
    return {name: headers[name] for name in names if name in headers}
