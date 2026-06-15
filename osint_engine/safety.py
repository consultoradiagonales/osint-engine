from __future__ import annotations

import re
from urllib.parse import quote_plus

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)(?:[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$"
)


class ScopeError(ValueError):
    """Raised when the requested target is outside the supported safe scope."""


def normalize_domain(value: str) -> str:
    domain = value.strip().lower()
    domain = domain.removeprefix("http://").removeprefix("https://")
    domain = domain.split("/", 1)[0].strip(".")
    if not DOMAIN_RE.match(domain):
        raise ScopeError(
            "Only public domain targets are supported in this version. "
            "Use a value like example.com."
        )
    return domain


def quote_query(value: str) -> str:
    return quote_plus(value)
