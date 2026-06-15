from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal

Confidence = Literal["High", "Medium", "Low"]
TargetType = Literal["domain"]


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


@dataclass(slots=True)
class Evidence:
    source: str
    claim: str
    value: str
    url: str | None = None
    confidence: Confidence = "Medium"
    collected_at: str = field(default_factory=utc_now_iso)
    raw: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "claim": self.claim,
            "value": self.value,
            "url": self.url,
            "confidence": self.confidence,
            "collected_at": self.collected_at,
            "raw": self.raw,
        }


@dataclass(slots=True)
class Finding:
    title: str
    detail: str
    confidence: Confidence = "Medium"
    evidence_sources: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "detail": self.detail,
            "confidence": self.confidence,
            "evidence_sources": self.evidence_sources,
        }


@dataclass(slots=True)
class Radiografia:
    target: str
    target_type: TargetType
    generated_at: str = field(default_factory=utc_now_iso)
    findings: list[Finding] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "target_type": self.target_type,
            "generated_at": self.generated_at,
            "findings": [finding.as_dict() for finding in self.findings],
            "evidence": [item.as_dict() for item in self.evidence],
            "errors": self.errors,
        }
