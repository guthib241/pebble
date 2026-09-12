"""Command-line interface."""

from __future__ import annotations

import argparse
import re
import sys
from typing import List, Optional, Sequence

from . import __version__
from .analysis import DEFAULT_DEFER_LIMIT_DAYS, analyse
from .cut import DEFAULT_NODE_BUDGET
from .plan import (
    Plan,
    PlanError,
    Task,
    load_plan,
    parse_duration,
    parse_moment,
    parse_plan,
)
from .report import render_json, render_text

EXIT_FITS = 0
EXIT_DOES_NOT_FIT = 1
EXIT_ERROR = 2

_ACCEPT_RE = re.compile(r"^(?P<name>.+?):(?P<estimate>[^@]+)@(?P<due>.+)$")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cutline",
        description="Decides whether your task list fits its deadlines, and what to cut.",
    )
    parser.add_argument("plan", nargs="?", help="plan file, or - to read standard input")
    parser.add_argument("--json", action="store_true", help="print JSON instead of text")
    parser.add_argument(
        "--schedule", action="store_true", help="also print the block-by-block schedule"
    )
    parser.add_argument(
        "--slack",
        action="store_true",
        help="also print spare capacity for new work, by deadline",
    )
    parser.add_argument(
        "--accept",
        metavar="NAME:DURATION@DUE",
        help='test taking on one more commitment, e.g. --accept "review:90m@2026-09-18 17:00"',
    )
    parser.add_argument(
        "--now",
        metavar="'YYYY-MM-DD HH:MM'",
        help="override the plan's own 'now' setting",
    )
    parser.add_argument(
        "--budget",
        type=int,
        default=DEFAULT_NODE_BUDGET,
        metavar="N",
        help=f"search nodes before giving up on proving the cut minimal "
        f"(default {DEFAULT_NODE_BUDGET})",
    )
    parser.add_argument(
        "--defer-limit-days",
        type=int,
        default=DEFAULT_DEFER_LIMIT_DAYS,
        metavar="N",
        help=f"how far ahead to look for a workable deadline (default "
        f"{DEFAULT_DEFER_LIMIT_DAYS})",
    )
    parser.add_argument(
        "--example", action="store_true", help="print an example plan file and exit"
    )
    parser.add_argument("--version", action="version", version=f"cutline {__version__}")
    return parser


EXAMPLE_PLAN = """\
# Everything cutline needs: when you can work, and what you have promised.
now: 2026-09-14 09:00

hours:
  mon-fri: 09:00-12:30, 13:30-17:30
  sat: 10:00-13:00

off: 2026-09-16

busy:
  2026-09-14 11:00-12:00  standup
  2026-09-15 14:00-15:30  dentist

tasks:
  spec draft        6h    due 2026-09-15 12:00  weight 3
  migration script  5h    due 2026-09-15 17:30  required
  code review       2h    due 2026-09-14 17:30  earliest 2026-09-14 13:30
  slides            3h    due 2026-09-15 17:30  weight 0.5
"""


def parse_accept(text: str, plan: Plan) -> Task:
    """Parse ``name:duration@due`` into a task, validated against the plan."""
    match = _ACCEPT_RE.match(text.strip())
    if match is None:
        raise PlanError(
            [f"--accept expects NAME:DURATION@DUE, for example 'review:90m@2026-09-18 17:00'"]
        )
    name = match.group("name").strip()
    if not name:
        raise PlanError(["--accept needs a task name"])
    if any(task.name == name for task in plan.tasks):
        raise PlanError([f"--accept name {name!r} is already used by a task in the plan"])
    try:
        estimate = parse_duration(match.group("estimate").strip())
    except ValueError as exc:
        raise PlanError([f"--accept: {exc}"]) from None
    try:
        due, _ = parse_moment(match.group("due").split(), end_of_day=True)
    except ValueError as exc:
        raise PlanError([f"--accept: {exc}"]) from None
    if due <= plan.now:
        raise PlanError(["--accept: the deadline is at or before the plan's 'now'"])
    return Task(name=name, estimate=estimate, due=due, line=0)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.example:
        print(EXAMPLE_PLAN, end="")
        return EXIT_FITS

    if not args.plan:
        parser.error("no plan file given; pass a path, - for standard input, or --example")
    if args.budget < 1:
        parser.error("--budget must be at least 1")
    if args.defer_limit_days < 1:
        parser.error("--defer-limit-days must be at least 1")

    try:
        if args.plan == "-":
            plan = parse_plan(sys.stdin.read())
            source = "standard input"
        else:
            plan = load_plan(args.plan)
            source = args.plan

        if args.now:
            moment, _ = parse_moment(args.now.split())
            plan = Plan(moment, dict(plan.hours), plan.busy, plan.off, plan.tasks)
            stale = [task.name for task in plan.tasks if task.due <= moment]
            if stale:
                raise PlanError(
                    [
                        "--now is at or after the deadline of: " + ", ".join(sorted(stale)),
                    ]
                )

        added: Optional[Task] = None
        if args.accept:
            added = parse_accept(args.accept, plan)
            plan = plan.with_tasks(list(plan.tasks) + [added])
    except PlanError as exc:
        for problem in exc.problems:
            print(f"cutline: {problem}", file=sys.stderr)
        return EXIT_ERROR
    except ValueError as exc:
        print(f"cutline: --now: {exc}", file=sys.stderr)
        return EXIT_ERROR

    analysis = analyse(
        plan,
        source=source,
        node_budget=args.budget,
        defer_limit_days=args.defer_limit_days,
        added=added,
    )

    if args.json:
        print(render_json(analysis))
    else:
        print(render_text(analysis, show_schedule=args.schedule, show_slack=args.slack))

    return EXIT_FITS if analysis.feasible else EXIT_DOES_NOT_FIT


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
