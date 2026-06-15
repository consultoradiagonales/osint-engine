from __future__ import annotations

from ..models import Evidence
from ..safety import quote_query


def collect_manual_queries(domain: str) -> list[Evidence]:
    quoted_domain = quote_query(domain)
    exact = quote_query(f'"{domain}"')
    queries = [
        (
            "google_exact_domain",
            f"https://www.google.com/search?q={exact}",
            "Exact-domain Google query for analyst review.",
        ),
        (
            "google_docs",
            "https://www.google.com/search?q="
            + quote_query(f'site:{domain} filetype:pdf OR filetype:xls OR filetype:doc'),
            "Public document search for the target domain.",
        ),
        (
            "bing_exact_domain",
            f"https://www.bing.com/search?q={exact}",
            "Exact-domain Bing query for analyst review.",
        ),
        (
            "github_code",
            f"https://github.com/search?q={quoted_domain}&type=code",
            "Public GitHub code search for domain exposure.",
        ),
        (
            "crtsh",
            f"https://crt.sh/?q=%25.{quoted_domain}",
            "Certificate Transparency search for subdomain leads.",
        ),
        (
            "wayback",
            f"https://web.archive.org/web/*/{quoted_domain}/*",
            "Wayback Machine historical URL search.",
        ),
    ]

    return [
        Evidence(
            source="manual-query",
            claim=name,
            value=description,
            url=url,
            confidence="High",
        )
        for name, url, description in queries
    ]
