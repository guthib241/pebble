"""Reproducible evidence run: scenarios, control checks and timing measurements.

Usage, from the project root:

    python3 evidence/run_evidence.py > evidence/results.md

Every number quoted in README.md comes from this script. It writes Markdown to
standard output and does not modify anything.
"""

from __future__ import annotations

import datetime as datetime_module
import platform
import random
import re
import subprocess
import sys
import time
from dataclasses import replace
from datetime import timedelta
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cutline.analysis import analyse  # noqa: E402
from cutline.cut import brute_force_cut, minimum_cut  # noqa: E402
from cutline.feasibility import edf_schedule, feasible  # noqa: E402
from cutline.plan import Busy, Plan, Task, load_plan  # noqa: E402
from tests.support import calendar_for, random_plan  # noqa: E402

SCENARIOS = ROOT / "evidence" / "scenarios"
EXPECT_RE = re.compile(r"#\s*expect:\s*(?P<verdict>.+)")

# Cloned by the timing generators below.
_TEMPLATE = Task(name="", estimate=60, due=datetime_module.datetime(2026, 9, 14, 17, 0))


def scenario_verdict(path: Path) -> str:
    """Run cutline on a scenario and describe the outcome in one line."""
    plan = load_plan(str(path))
    analysis = analyse(plan, source=str(path))
    if analysis.feasible:
        return "fits"
    if analysis.cut.impossible:
        return "impossible"
    return "cut " + ", ".join(analysis.cut.dropped)


def expected_verdict(path: Path) -> Optional[str]:
    for line in path.read_text(encoding="utf-8").splitlines():
        match = EXPECT_RE.search(line)
        if match:
            return match.group("verdict").strip()
    return None


def run_scenarios() -> Tuple[int, int, List[str]]:
    matched = 0
    total = 0
    failures: List[str] = []
    for path in sorted(SCENARIOS.glob("*.txt")):
        expected = expected_verdict(path)
        if expected is None:
            failures.append(f"{path.name}: no '# expect:' line")
            continue
        total += 1
        actual = scenario_verdict(path)
        if actual == expected:
            matched += 1
        else:
            failures.append(f"{path.name}: expected {expected!r}, got {actual!r}")
    return matched, total, failures


def control_methods_agree(instances: int = 500) -> Tuple[int, int, int, int]:
    """The window condition and the EDF schedule must give the same verdict."""
    rng = random.Random(20260912)
    agree = 0
    fits = 0
    does_not = 0
    disagree = 0
    for _ in range(instances):
        plan = random_plan(rng, rng.randint(1, 8))
        calendar = calendar_for(plan)
        by_windows = feasible(plan.tasks, calendar)
        by_schedule = edf_schedule(plan.tasks, calendar).feasible
        if by_windows == by_schedule:
            agree += 1
        else:
            disagree += 1
        if by_windows:
            fits += 1
        else:
            does_not += 1
    return agree, disagree, fits, does_not


def control_optimality(instances: int = 200) -> Tuple[int, int, int]:
    """The branch and bound must match exhaustive enumeration."""
    rng = random.Random(4242)
    checked = 0
    equal = 0
    infeasible = 0
    for _ in range(instances):
        plan = random_plan(rng, rng.randint(2, 7))
        calendar = calendar_for(plan)
        if not feasible(plan.tasks, calendar):
            infeasible += 1
        exact = brute_force_cut(plan.tasks, calendar)
        found = minimum_cut(plan.tasks, calendar)
        checked += 1
        if abs(found.weight - exact.weight) < 1e-9 and found.impossible == exact.impossible:
            equal += 1
    return checked, equal, infeasible


def _shift(plan: Plan, days: int) -> Plan:
    """Move an entire plan by whole weeks, which preserves every weekday."""
    delta = timedelta(days=days)
    return Plan(
        now=plan.now + delta,
        hours=dict(plan.hours),
        busy=tuple(
            Busy(start=block.start + delta, end=block.end + delta, label=block.label)
            for block in plan.busy
        ),
        off=frozenset(day + delta for day in plan.off),
        tasks=tuple(
            replace(
                task,
                due=task.due + delta,
                earliest=(task.earliest + delta) if task.earliest is not None else None,
            )
            for task in plan.tasks
        ),
    )


def control_invariances(instances: int = 200) -> Tuple[int, int, int]:
    """Two changes that must not matter: task order, and shifting the plan a week.

    Both are controls in the strict sense: the inputs differ in a way that cannot
    affect the answer, so any difference in the answer is a bug.
    """
    rng = random.Random(777)
    checked = 0
    order_same = 0
    shift_same = 0
    for _ in range(instances):
        plan = random_plan(rng, rng.randint(2, 6))
        base = analyse(plan)
        checked += 1

        shuffled = list(plan.tasks)
        rng.shuffle(shuffled)
        reordered = analyse(plan.with_tasks(shuffled))
        if (
            reordered.feasible == base.feasible
            and reordered.cut.dropped == base.cut.dropped
            and abs(reordered.cut.weight - base.cut.weight) < 1e-9
        ):
            order_same += 1

        shifted = analyse(_shift(plan, 7))
        if (
            shifted.feasible == base.feasible
            and shifted.cut.dropped == base.cut.dropped
            and abs(shifted.cut.weight - base.cut.weight) < 1e-9
        ):
            shift_same += 1
    return checked, order_same, shift_same


def control_determinism() -> Tuple[int, int]:
    """Running the same scenario twice must produce byte-identical output."""
    same = 0
    total = 0
    for path in sorted(SCENARIOS.glob("*.txt")):
        total += 1
        first = subprocess.run(
            [sys.executable, "-m", "cutline", str(path), "--json", "--schedule"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        ).stdout
        second = subprocess.run(
            [sys.executable, "-m", "cutline", str(path), "--json", "--schedule"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        ).stdout
        if first == second:
            same += 1
    return total, same


def stress_plan(rng: random.Random, count: int, overload: float = 1.2) -> Plan:
    """A plan that forces the cut search to work.

    No required tasks, and estimates scaled so the total commitment is ``overload``
    times the capacity before the last deadline, which guarantees an infeasible plan
    that a cut can actually fix.
    """
    from datetime import time as clock_time

    from tests.support import MONDAY, at

    hours = {day: ((clock_time(9, 0), clock_time(17, 0)),) for day in range(0, 5)}
    deadlines = [at(day, hour) for day in range(0, 5) for hour in (12, 17)]
    tasks = []
    for index in range(count):
        tasks.append(
            replace(
                _TEMPLATE,
                name=f"task {index:02d}",
                estimate=rng.choice([30, 45, 60, 90, 120]),
                due=rng.choice(deadlines),
                weight=rng.choice([0.5, 1.0, 2.0, 3.0]),
            )
        )
    plan = Plan(now=MONDAY, hours=hours, busy=(), off=frozenset(), tasks=tuple(tasks))
    calendar = calendar_for(plan)
    capacity = calendar.capacity(0, calendar.minutes(plan.horizon()))
    committed = sum(task.estimate for task in tasks)
    if committed == 0:
        return plan
    scale = (capacity * overload) / committed
    scaled = tuple(
        replace(task, estimate=max(15, int(round(task.estimate * scale))))
        for task in tasks
    )
    return plan.with_tasks(scaled)


def hard_plan(count: int) -> Plan:
    """Many interchangeable tasks in one over-subscribed window: the worst case."""
    from datetime import time as clock_time

    from tests.support import MONDAY, at

    hours = {0: ((clock_time(9, 0), clock_time(17, 0)),)}
    tasks = tuple(
        replace(_TEMPLATE, name=f"same {index:02d}", estimate=60, due=at(0, 17))
        for index in range(count)
    )
    return Plan(now=MONDAY, hours=hours, busy=(), off=frozenset(), tasks=tasks)


def timing(task_counts=(10, 20, 40, 80)) -> List[Tuple[str, int, float, int, str, bool]]:
    """Wall clock for one full analysis, on plans that exercise the cut search."""
    results: List[Tuple[str, int, float, int, str, bool]] = []
    for count in task_counts:
        rng = random.Random(1000 + count)
        plan = stress_plan(rng, count)
        start = time.perf_counter()
        analysis = analyse(plan)
        elapsed = time.perf_counter() - start
        verdict = (
            "fits"
            if analysis.feasible
            else ("impossible" if analysis.cut.impossible else f"cut {len(analysis.cut.dropped)}")
        )
        results.append(
            ("overloaded by 20%", count, elapsed, analysis.cut.nodes, verdict,
             analysis.cut.proven_minimal)
        )
    for count in (12, 20):
        plan = hard_plan(count)
        start = time.perf_counter()
        analysis = analyse(plan)
        elapsed = time.perf_counter() - start
        verdict = (
            "fits"
            if analysis.feasible
            else ("impossible" if analysis.cut.impossible else f"cut {len(analysis.cut.dropped)}")
        )
        results.append(
            ("identical tasks, one deadline", count, elapsed, analysis.cut.nodes, verdict,
             analysis.cut.proven_minimal)
        )
    return results


def git_commit() -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() or "unknown"


def main() -> int:
    print("# cutline evidence run\n")
    print(f"- Date (UTC): {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}")
    print(f"- Commit: {git_commit()}")
    print(f"- Python: {platform.python_version()} ({platform.python_implementation()})")
    print(f"- Platform: {platform.platform()}")
    print("- Command: `python3 evidence/run_evidence.py`\n")

    matched, total, failures = run_scenarios()
    print("## Scenarios\n")
    print(
        f"Each file in `evidence/scenarios/` states its expected outcome on a "
        f"`# expect:` line: whether the plan fits, which tasks the cheapest cut drops, "
        f"or that no cut can fix it.\n"
    )
    print(f"- Scenarios: {total}")
    print(f"- Outcome matched the expectation: {matched}")
    print(f"- Mismatches: {len(failures)}")
    for failure in failures:
        print(f"  - {failure}")
    print()

    print("## Control checks\n")
    agree, disagree, fits, does_not = control_methods_agree()
    print(
        f"1. **Two independent feasibility methods.** On {agree + disagree} random plans "
        f"the window condition and the earliest-deadline-first schedule agreed "
        f"{agree} times and disagreed {disagree} times "
        f"({fits} of the instances fit, {does_not} did not). The two methods share no "
        f"code beyond the calendar, so agreement is a real check rather than a "
        f"restatement.\n"
    )
    checked, equal, infeasible = control_optimality()
    print(
        f"2. **Optimality against exhaustive enumeration.** On {checked} random plans "
        f"({infeasible} of them infeasible) the branch-and-bound cut matched the "
        f"minimum-weight cut found by enumerating every subset in {equal} cases.\n"
    )
    invariance_checked, order_same, shift_same = control_invariances()
    print(
        f"3. **Invariance controls.** Two changes that cannot affect the answer: "
        f"reordering the task list, and moving the whole plan forward by exactly one "
        f"week. Over {invariance_checked} random plans the verdict and the cut were "
        f"unchanged in {order_same} reorderings and {shift_same} week shifts.\n"
    )
    determinism_total, determinism_same = control_determinism()
    print(
        f"4. **Determinism.** Each of the {determinism_total} scenarios was run twice "
        f"through the command line; {determinism_same} produced byte-identical output.\n"
    )

    print("## Timing\n")
    print("One full analysis (feasibility, certificate, cut search, deferral advice) "
          "per row:\n")
    print("| Plan shape | Tasks | Wall clock | Search nodes | Outcome | Proven minimal |")
    print("| --- | --- | --- | --- | --- | --- |")
    for shape, count, elapsed, nodes, verdict, proven in timing():
        print(
            f"| {shape} | {count} | {elapsed:.3f} s | {nodes} | {verdict} | "
            f"{'yes' if proven else 'no'} |"
        )
    print()
    print("The first rows use plans deliberately overloaded by 20% so that a cut is "
          "needed and the search runs; the last rows use the worst case for the search, "
          "many identical tasks sharing one deadline. Generators are seeded, so the "
          "numbers are reproducible on the same machine, and they describe these "
          "instances only. Where a plan exhausts the node budget the tool says so "
          "instead of claiming minimality.")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
