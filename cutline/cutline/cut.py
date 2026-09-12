"""Choosing what to cut when a plan does not fit.

The search rests on one observation: an over-subscribed window (see
:mod:`cutline.feasibility`) contains tasks that cannot all fit inside it, so every way
of making the plan feasible must cut at least one task from that window. Branching over
the tasks of one violated window is therefore complete, and with cost-based pruning the
search returns a minimum-weight cut.

Tasks marked ``required`` are never cut. A window whose tasks are all required cannot be
fixed, which ends that branch.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from .capacity import Calendar
from .feasibility import earliest_feasible_deadline, feasible, violated_windows
from .plan import Task

DEFAULT_NODE_BUDGET = 200_000


@dataclass(frozen=True)
class Cut:
    """A set of tasks to cut, and how sure we are that it is the cheapest one."""

    dropped: Tuple[str, ...] = ()
    weight: float = 0.0
    proven_minimal: bool = True
    nodes: int = 0
    budget_exhausted: bool = False
    impossible: bool = False

    @property
    def empty(self) -> bool:
        return not self.dropped


def _weight(names: Sequence[str], by_name: Dict[str, Task]) -> float:
    return float(sum(by_name[name].weight for name in names))


def greedy_cut(tasks: Sequence[Task], calendar: Calendar) -> List[str]:
    """A quick cut, used as the starting bound for the exact search.

    Repeatedly takes the most over-subscribed window and cuts the task that frees the
    most time per unit of weight, in the spirit of the Moore-Hodgson rule of discarding
    the longest job when a deadline breaks.
    """
    by_name = {task.name: task for task in tasks}
    kept = list(tasks)
    dropped: List[str] = []
    while True:
        windows = violated_windows(kept, calendar)
        if not windows:
            return sorted(dropped)
        candidates: Optional[List[str]] = None
        for window in windows:
            options = [name for name in window.tasks if not by_name[name].required]
            if options:
                candidates = options
                break
        if candidates is None:
            return sorted(dropped)
        choice = max(
            candidates,
            key=lambda name: (
                by_name[name].estimate / by_name[name].weight,
                by_name[name].estimate,
                name,
            ),
        )
        dropped.append(choice)
        kept = [task for task in kept if task.name != choice]


def minimum_cut(
    tasks: Sequence[Task],
    calendar: Calendar,
    node_budget: int = DEFAULT_NODE_BUDGET,
) -> Cut:
    """The cheapest set of tasks to cut so that the rest fits.

    Returns a :class:`Cut` whose ``proven_minimal`` is true when the search finished, and
    false when it hit ``node_budget`` first, in which case the cut is valid but may not
    be the cheapest.
    """
    by_name = {task.name: task for task in tasks}
    if feasible(tasks, calendar):
        return Cut()

    required = [task for task in tasks if task.required]
    if not feasible(required, calendar):
        optional = tuple(sorted(task.name for task in tasks if not task.required))
        return Cut(
            dropped=optional,
            weight=_weight(optional, by_name),
            proven_minimal=True,
            nodes=0,
            impossible=True,
        )

    best_names = tuple(greedy_cut(tasks, calendar))
    best_weight = _weight(best_names, by_name)

    nodes = 0
    exhausted = False
    seen = set()
    stack: List[Tuple[frozenset, float]] = [(frozenset(), 0.0)]

    while stack:
        if nodes >= node_budget:
            exhausted = True
            break
        dropped, cost = stack.pop()
        if dropped in seen or cost >= best_weight:
            continue
        seen.add(dropped)
        nodes += 1

        kept = [task for task in tasks if task.name not in dropped]
        windows = violated_windows(kept, calendar)
        if not windows:
            best_names = tuple(sorted(dropped))
            best_weight = cost
            continue

        branch: Optional[List[str]] = None
        dead_end = False
        for window in windows:
            options = [name for name in window.tasks if not by_name[name].required]
            if not options:
                dead_end = True
                break
            if branch is None or len(options) < len(branch):
                branch = options
        if dead_end or branch is None:
            continue

        ordered = sorted(
            branch,
            key=lambda name: (by_name[name].weight, -by_name[name].estimate, name),
        )
        for name in reversed(ordered):
            child_cost = cost + by_name[name].weight
            if child_cost < best_weight:
                stack.append((dropped | {name}, child_cost))

    return Cut(
        dropped=tuple(sorted(best_names)),
        weight=best_weight,
        proven_minimal=not exhausted,
        nodes=nodes,
        budget_exhausted=exhausted,
    )


def brute_force_cut(tasks: Sequence[Task], calendar: Calendar) -> Cut:
    """Exhaustive reference implementation, for tests and very small plans.

    Enumerates every subset of the cuttable tasks and keeps the feasible one of least
    weight. Exponential by construction; used to confirm that :func:`minimum_cut`
    really returns a minimum-weight answer.
    """
    by_name = {task.name: task for task in tasks}
    cuttable = [task.name for task in tasks if not task.required]
    best: Optional[Tuple[float, Tuple[str, ...]]] = None
    for mask in range(1 << len(cuttable)):
        names = tuple(cuttable[index] for index in range(len(cuttable)) if mask >> index & 1)
        weight = _weight(names, by_name)
        if best is not None and weight > best[0]:
            continue
        chosen = set(names)
        kept = [task for task in tasks if task.name not in chosen]
        if feasible(kept, calendar):
            candidate = (weight, tuple(sorted(names)))
            if best is None or candidate < best:
                best = candidate
    if best is None:
        optional = tuple(sorted(cuttable))
        return Cut(
            dropped=optional,
            weight=_weight(optional, by_name),
            proven_minimal=True,
            impossible=True,
        )
    return Cut(dropped=best[1], weight=best[0], proven_minimal=True)


def deferrals(
    tasks: Sequence[Task],
    calendar: Calendar,
    cut: Cut,
    limit_minutes: int,
) -> Dict[str, Optional[int]]:
    """For each cut task, the earliest deadline that would let it stay.

    The other cut tasks are assumed to stay cut, so the answer reads as "this task can
    come back if you move it to this time". ``None`` means no deadline within
    ``limit_minutes`` is enough.
    """
    kept = [task for task in tasks if task.name not in cut.dropped]
    answers: Dict[str, Optional[int]] = {}
    for name in cut.dropped:
        target = next(task for task in tasks if task.name == name)
        answers[name] = earliest_feasible_deadline(
            kept + [target], calendar, name, limit_minutes
        )
    return answers
