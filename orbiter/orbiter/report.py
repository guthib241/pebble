"""Output formatting."""

from __future__ import annotations

import json
from collections import Counter
from typing import Sequence

from .analyze import AnalysisError, Diagnostic
from .config import CODES
from .units import BASE_UNIT_NAME, LEXICON


def format_text(
    diagnostics: Sequence[Diagnostic], errors: Sequence[AnalysisError], files: int
) -> str:
    lines = [str(diagnostic) for diagnostic in diagnostics]
    lines.extend(str(error) for error in errors)
    counts = Counter(diagnostic.code for diagnostic in diagnostics)
    if diagnostics:
        lines.append("")
        for code in sorted(counts):
            lines.append(f"{code} {CODES.get(code, '')}: {counts[code]}")
    summary = f"{len(diagnostics)} finding(s) in {files} file(s)"
    if errors:
        summary += f", {len(errors)} file(s) could not be analysed"
    lines.append(summary)
    return "\n".join(lines)


def format_json(
    diagnostics: Sequence[Diagnostic], errors: Sequence[AnalysisError], files: int
) -> str:
    payload = {
        "files_analysed": files,
        "findings": [diagnostic.as_dict() for diagnostic in diagnostics],
        "errors": [error.as_dict() for error in errors],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def format_units() -> str:
    """The unit lexicon, grouped by dimension."""
    by_dimension: dict[str, dict[str, list[str]]] = {}
    for token, unit in LEXICON.items():
        by_dimension.setdefault(unit.dimension, {}).setdefault(unit.label, []).append(token)
    lines = []
    for dimension in sorted(by_dimension):
        lines.append(f"{dimension} (base unit: {BASE_UNIT_NAME[dimension]})")
        units = by_dimension[dimension]
        for label in sorted(units, key=lambda item: len(item)):
            tokens = ", ".join(sorted(units[label]))
            lines.append(f"  {label}: {tokens}")
        lines.append("")
    lines.append("Checks:")
    for code in sorted(CODES):
        lines.append(f"  {code}  {CODES[code]}")
    return "\n".join(lines)
