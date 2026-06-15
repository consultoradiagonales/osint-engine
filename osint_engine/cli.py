from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .engine import EngineOptions, run_domain_radiografia
from .report import write_reports
from .safety import ScopeError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="osint-engine",
        description="Generate evidence-backed OSINT radiografias from public sources.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    domain = subparsers.add_parser("domain", help="Run a safe public-domain OSINT scan.")
    domain.add_argument("target", help="Domain to investigate, for example example.com.")
    domain.add_argument(
        "--out",
        default="outputs/radiografia",
        help="Output path without extension. Defaults to outputs/radiografia.",
    )
    domain.add_argument("--offline", action="store_true", help="Do not call network sources.")
    domain.add_argument(
        "--with-theharvester",
        action="store_true",
        help="Attach optional theHarvester CLI output if the tool is installed.",
    )
    domain.add_argument("--timeout", type=float, default=12.0, help="HTTP/DNS timeout in seconds.")
    domain.add_argument("--limit", type=int, default=50, help="Maximum rows per collector.")
    domain.add_argument("--json-only", action="store_true", help="Only write JSON output.")
    domain.add_argument("--markdown-only", action="store_true", help="Only write Markdown output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.json_only and args.markdown_only:
        parser.error("--json-only and --markdown-only cannot be used together.")

    if args.command == "domain":
        try:
            report = run_domain_radiografia(
                args.target,
                EngineOptions(
                    offline=args.offline,
                    include_theharvester=args.with_theharvester,
                    timeout=args.timeout,
                    limit=args.limit,
                ),
            )
        except ScopeError as exc:
            print(f"Scope error: {exc}", file=sys.stderr)
            return 2

        written = write_reports(
            report,
            Path(args.out),
            write_json=not args.markdown_only,
            write_markdown=not args.json_only,
        )
        for path in written:
            print(path)
        if report.errors:
            print("Completed with non-fatal collector errors:", file=sys.stderr)
            for error in report.errors:
                print(f"- {error}", file=sys.stderr)
        return 0

    parser.error("Unknown command")
    return 2
