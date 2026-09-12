"""Human-readable and JSON output."""

from __future__ import annotations

import json
import math

from .analyze import Report

RULE_TITLES = {
    "BF001": "retry amplification",
    "BF002": "unbounded retry",
    "BF003": "retry without backoff",
    "BF004": "no timeout under retry",
    "BF005": "budget exceeded",
}

COLORS = {"error": "\033[31m", "warning": "\033[33m", "info": "\033[36m"}
RESET = "\033[0m"


def _number(value: float) -> str:
    if math.isinf(value):
        return "unbounded"
    return str(int(value)) if float(value).is_integer() else f"{value:.2f}"


def render_text(report: Report, color: bool = False, show_evidence: bool = True) -> str:
    lines: list[str] = []
    for finding in report.findings:
        label = finding.severity.upper()
        if color:
            label = f"{COLORS.get(finding.severity, '')}{label}{RESET}"
        title = RULE_TITLES.get(finding.rule, finding.rule)
        lines.append(f"{finding.location}: {label} {finding.rule} ({title}): {finding.message}")
        if show_evidence:
            for item in finding.evidence:
                lines.append(f"    via {item}")
    counts = summarize(report)
    if not report.findings:
        lines.append("No retry amplification findings.")
    lines.append("")
    lines.append(
        "{functions} functions, {edges} resolved call edges, {retry_sites} retry sites; "
        "{errors} errors, {warnings} warnings, {infos} info".format(
            functions=report.stats.get("functions", 0),
            edges=report.stats.get("edges", 0),
            retry_sites=report.stats.get("retry_sites", 0),
            **counts,
        )
    )
    return "\n".join(lines)


def summarize(report: Report) -> dict:
    counts = {"errors": 0, "warnings": 0, "infos": 0}
    for finding in report.findings:
        key = {"error": "errors", "warning": "warnings", "info": "infos"}[finding.severity]
        counts[key] += 1
    return counts


def render_json(report: Report) -> str:
    payload = {
        "findings": [
            {
                "rule": finding.rule,
                "severity": finding.severity,
                "message": finding.message,
                "file": finding.location.file,
                "line": finding.location.line,
                "evidence": finding.evidence,
                "data": {
                    key: (_number(value) if isinstance(value, float) else value)
                    for key, value in finding.data.items()
                },
            }
            for finding in report.findings
        ],
        "hot_paths": [
            {
                "call": record.call.detail,
                "file": record.location.file,
                "line": record.location.line,
                "attempts": _number(record.attempts),
                "estimated": not record.known,
                "path": record.path,
            }
            for record in report.amplifications[:20]
        ],
        "stats": {**report.stats, **summarize(report)},
    }
    return json.dumps(payload, indent=2, sort_keys=True)
