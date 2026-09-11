"""Command line entry point."""

from __future__ import annotations

import argparse
import os
import sys

from . import __version__, config, graph, parse, report
from .analyze import Options, analyze
from .model import SEVERITY_ORDER

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="backfire",
        description="Find retry amplification and timeout blowups in Python code.",
    )
    parser.add_argument("paths", nargs="*", default=["."], help="files or directories to scan")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    parser.add_argument(
        "--max-attempts",
        type=float,
        default=None,
        help="report a call reachable with more than this many composed attempts (default 10)",
    )
    parser.add_argument("--max-depth", type=int, default=None, help="maximum call-path depth to follow")
    parser.add_argument(
        "--budget",
        action="append",
        default=[],
        metavar="FUNC=DURATION",
        help="worst-case time budget for an entry point, e.g. api.handler=10s",
    )
    parser.add_argument("--exclude", action="append", default=[], metavar="DIR", help="directory to skip")
    parser.add_argument(
        "--resolve-by-name",
        action="store_true",
        help="also resolve calls by unique function name (more edges, lower precision)",
    )
    parser.add_argument("--config", default=None, help="path to a backfire.toml (default: auto-discover)")
    parser.add_argument("--no-config", action="store_true", help="ignore any config file")
    parser.add_argument(
        "--fail-on",
        choices=["none", "info", "warning", "error"],
        default="error",
        help="exit non-zero when a finding at this severity or above exists (default error)",
    )
    parser.add_argument("--no-evidence", action="store_true", help="hide the 'via' evidence lines")
    parser.add_argument("--no-color", action="store_true", help="disable colored severities")
    parser.add_argument("--version", action="version", version=f"backfire {__version__}")
    return parser


def _budget_pairs(values, parser):
    budgets = {}
    for item in values:
        name, _, duration = item.partition("=")
        if not name or not duration:
            parser.error(f"--budget expects FUNC=DURATION, got {item!r}")
        try:
            budgets[name] = config.parse_duration(duration)
        except config.ConfigError as error:
            parser.error(str(error))
    return budgets


def _drop_suppressed(findings, modules):
    """Honour '# backfire: ignore' comments on the reported line."""
    by_file = {module.path: module.suppressions for module in modules if module.suppressions}
    kept = []
    for finding in findings:
        rules = by_file.get(finding.location.file, {}).get(finding.location.line, ())
        if rules is None or (rules and finding.rule in rules):
            continue
        kept.append(finding)
    return kept


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    paths = args.paths or ["."]
    for path in paths:
        if not os.path.exists(path):
            parser.error(f"path does not exist: {path}")

    settings: dict = {}
    if not args.no_config:
        config_path = args.config or config.find_config(paths[0])
        if config_path:
            try:
                settings = config.load(config_path)
            except (config.ConfigError, OSError, ValueError) as error:
                print(f"backfire: cannot read config {config_path}: {error}", file=sys.stderr)
                return EXIT_USAGE

    excludes = set(parse.DEFAULT_EXCLUDES) | set(settings.get("exclude", [])) | set(args.exclude)
    budgets = dict(settings.get("budgets", {}))
    budgets.update(_budget_pairs(args.budget, parser))
    options = Options(
        max_attempts=args.max_attempts
        if args.max_attempts is not None
        else settings.get("max_attempts", Options().max_attempts),
        max_depth=args.max_depth if args.max_depth is not None else settings.get("max_depth", Options().max_depth),
        budgets=budgets,
    )
    resolve_by_name = args.resolve_by_name or settings.get("resolve_by_name", False)

    modules = parse.parse_project(paths, excludes=excludes)
    for module in modules:
        if module.parse_error:
            print(f"backfire: skipped {module.path}: {module.parse_error}", file=sys.stderr)
    call_graph = graph.build(modules, resolve_by_name=resolve_by_name)
    result = analyze(call_graph, options)
    result.findings = _drop_suppressed(result.findings, modules)
    result.stats["files"] = len(modules)
    result.stats["unparsed_files"] = sum(1 for module in modules if module.parse_error)

    if args.json:
        print(report.render_json(result))
    else:
        color = not args.no_color and sys.stdout.isatty()
        print(report.render_text(result, color=color, show_evidence=not args.no_evidence))

    if args.fail_on == "none":
        return EXIT_OK
    threshold = SEVERITY_ORDER[args.fail_on]
    if any(SEVERITY_ORDER[finding.severity] >= threshold for finding in result.findings):
        return EXIT_FINDINGS
    return EXIT_OK


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
