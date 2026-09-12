"""Command-line interface."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional, Sequence

from . import __version__
from .analyze import analyze_paths, collect_python_files
from .config import CODES, ConfigError, load_config
from .report import format_json, format_text, format_units

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_ERROR = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="orbiter",
        description="Flags Python code that mixes units, like milliseconds passed as seconds.",
    )
    parser.add_argument("paths", nargs="*", help="files or directories to analyse")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format (default: text)",
    )
    parser.add_argument(
        "--disable",
        action="append",
        default=[],
        metavar="CODE",
        help=f"disable a check; one of {', '.join(sorted(CODES))}",
    )
    parser.add_argument(
        "--strict-binary-prefixes",
        action="store_true",
        help="report kilobyte/kibibyte style mismatches (1000 vs 1024) as well",
    )
    parser.add_argument("--config", metavar="PATH", help="TOML configuration file")
    parser.add_argument(
        "--list-units", action="store_true", help="print the unit lexicon and exit"
    )
    parser.add_argument("--version", action="version", version=f"orbiter {__version__}")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_units:
        print(format_units())
        return EXIT_CLEAN

    if not args.paths:
        parser.error("no paths given")

    unknown: List[str] = [code for code in args.disable if code not in CODES]
    if unknown:
        parser.error(f"unknown check code(s): {', '.join(unknown)}")

    try:
        config = load_config(
            args.config,
            disable=frozenset(args.disable),
            strict_binary_prefixes=args.strict_binary_prefixes,
        )
    except ConfigError as exc:
        print(f"orbiter: {exc}", file=sys.stderr)
        return EXIT_ERROR

    files, _ = collect_python_files(args.paths)
    diagnostics, errors = analyze_paths(args.paths, config)

    if args.format == "json":
        print(format_json(diagnostics, errors, len(files)))
    else:
        print(format_text(diagnostics, errors, len(files)))

    if errors:
        return EXIT_ERROR
    return EXIT_FINDINGS if diagnostics else EXIT_CLEAN


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
