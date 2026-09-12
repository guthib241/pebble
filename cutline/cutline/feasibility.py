"""Deciding whether a set of tasks fits, by two independent methods.

Work is treated as divisible: a task may be split across any number of free blocks.
Under that assumption both methods below decide feasibility exactly, and they must
always agree.

* :func:`edf_schedule` runs preemptive earliest-deadline-first over the calendar and
  reports which tasks finish late. Preemptive EDF is optimal for a single resource with
  release times, so a late task means no schedule exists.
* :func:`violated_windows` checks the window condition: for every interval bounded by a
  release time and a deadline, the work that can only run inside that interval must not
  exceed the interval's capacity. A violation is a certificate of infeasibility that a
  reader can check by hand.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from .capacity import Calendar
from .plan import Task


@dataclass(frozen=True)
class Block:
    """A stretch of time assigned to one task."""

    task: str
    start: int
    end: int

    @property
    def minutes(self) -> int:
        return self.end - self.start


@dataclass(frozen=True)
class Schedule:
    blocks: Tuple[Block, ...]
    late: Tuple[str, ...]
    shortfall: Dict[str, int]
    finish: Dict[str, int]

    @property
    def feasible(self) -> bool:
        return not self.late


@dataclass(frozen=True)
class Window:
    """An over-subscribed interval: a checkable certificate of infeasibility."""

    start: int
    end: int
    tasks: Tuple[str, ...]
    work: int
    capacity: int

    @property
    def deficit(self) -> int:
        return self.work - self.capacity

    def sort_key(self) -> Tuple[int, int, int, int]:
        """Most severe first: biggest deficit, then tightest and earliest window."""
        return (-self.deficit, self.end - self.start, self.start, len(self.tasks))


@dataclass(frozen=True)
class _Item:
    name: str
    release: int
    due: int
    estimate: int


def _items(tasks: Sequence[Task], calendar: Calendar) -> List[_Item]:
    items = []
    for task in tasks:
        release = max(0, calendar.minutes(task.release(calendar.origin)))
        items.append(
            _Item(
                name=task.name,
                release=release,
                due=calendar.minutes(task.due),
                estimate=task.estimate,
            )
        )
    return items


def merge_blocks(blocks: Sequence[Block]) -> List[Block]:
    """Join consecutive blocks belonging to the same task."""
    merged: List[Block] = []
    for block in blocks:
        if merged and merged[-1].task == block.task and merged[-1].end == block.start:
            merged[-1] = Block(block.task, merged[-1].start, block.end)
        else:
            merged.append(block)
    return merged


def edf_schedule(tasks: Sequence[Task], calendar: Calendar) -> Schedule:
    """Schedule by preemptive earliest deadline first over the free intervals."""
    items = _items(tasks, calendar)
    if not items:
        return Schedule((), (), {}, {})

    remaining = {item.name: item.estimate for item in items}
    release = {item.name: item.release for item in items}
    due = {item.name: item.due for item in items}
    # Deterministic priority: earliest deadline, then earliest release, then name.
    priority = {item.name: (item.due, item.release, item.name) for item in items}

    blocks: List[Block] = []
    finish: Dict[str, int] = {}

    for interval_start, interval_end in calendar.free:
        point = interval_start
        while point < interval_end:
            ready = [
                name
                for name, left in remaining.items()
                if left > 0 and release[name] <= point < due[name]
            ]
            if not ready:
                upcoming = [
                    release[name]
                    for name, left in remaining.items()
                    if left > 0 and release[name] > point and due[name] > point
                ]
                point = min([interval_end] + [value for value in upcoming if value > point])
                continue
            name = min(ready, key=lambda candidate: priority[candidate])
            limit = min(interval_end, point + remaining[name], due[name])
            for other, left in remaining.items():
                if (
                    left > 0
                    and release[other] > point
                    and due[other] > point
                    and priority[other] < priority[name]
                ):
                    limit = min(limit, release[other])
            blocks.append(Block(name, point, limit))
            remaining[name] -= limit - point
            if remaining[name] == 0:
                finish[name] = limit
            point = limit

    late = tuple(sorted(name for name, left in remaining.items() if left > 0))
    shortfall = {name: remaining[name] for name in late}
    return Schedule(tuple(merge_blocks(blocks)), late, shortfall, finish)


def violated_windows(tasks: Sequence[Task], calendar: Calendar) -> List[Window]:
    """Every over-subscribed window, most severe first.

    An empty result means the task set is feasible.
    """
    items = _items(tasks, calendar)
    if not items:
        return []
    found: List[Window] = []
    for item in items:
        if item.release >= item.due:
            # No time exists for this task at all. The parser rejects such plans, but
            # a caller building tasks directly can still produce one, and both
            # feasibility methods must agree about it.
            found.append(
                Window(
                    start=item.release,
                    end=item.due,
                    tasks=(item.name,),
                    work=item.estimate,
                    capacity=0,
                )
            )
    starts = sorted({0} | {item.release for item in items})
    for start in starts:
        candidates = sorted(
            (item.due, item.estimate, item.name)
            for item in items
            if item.release >= start
        )
        work = 0
        names: List[str] = []
        for index, (end, estimate, name) in enumerate(candidates):
            work += estimate
            names.append(name)
            # Only the last task sharing a deadline defines the window.
            if index + 1 < len(candidates) and candidates[index + 1][0] == end:
                continue
            if end <= start:
                continue
            available = calendar.capacity(start, end)
            if work > available:
                found.append(
                    Window(
                        start=start,
                        end=end,
                        tasks=tuple(sorted(names)),
                        work=work,
                        capacity=available,
                    )
                )
    found.sort(key=Window.sort_key)
    return found


def feasible(tasks: Sequence[Task], calendar: Calendar) -> bool:
    """Whether every task can finish by its deadline. Exact for divisible work."""
    return not violated_windows(tasks, calendar)


def worst_window(tasks: Sequence[Task], calendar: Calendar) -> Optional[Window]:
    windows = violated_windows(tasks, calendar)
    return windows[0] if windows else None


def slack_by_deadline(
    tasks: Sequence[Task], calendar: Calendar
) -> List[Tuple[int, int]]:
    """Spare capacity for new work, per distinct deadline.

    The value for deadline ``d`` is how many minutes of new work, startable now and due
    by ``d``, could still be added without making the plan infeasible. It is the
    smallest surplus over all windows ending at or after ``d``, because new work due by
    ``d`` also falls inside every later window.
    """
    items = _items(tasks, calendar)
    deadlines = sorted({item.due for item in items})
    if not deadlines:
        horizon = calendar.minutes(calendar.horizon)
        return [(horizon, calendar.capacity(0, horizon))]
    surplus: List[Tuple[int, int]] = []
    for deadline in deadlines:
        work = sum(item.estimate for item in items if item.due <= deadline)
        surplus.append((deadline, calendar.capacity(0, deadline) - work))
    result: List[Tuple[int, int]] = []
    running = None
    for deadline, value in reversed(surplus):
        running = value if running is None else min(running, value)
        result.append((deadline, running))
    result.reverse()
    return result


def earliest_feasible_deadline(
    tasks: Sequence[Task],
    calendar: Calendar,
    name: str,
    limit: int,
) -> Optional[int]:
    """Earliest new deadline for ``name`` that makes the whole set feasible.

    Feasibility is monotone in this deadline: moving it later only relaxes the
    constraints, so the answer is found by binary search. Returns ``None`` when no
    deadline up to ``limit`` works, which means other tasks are also over-committed.
    """
    from dataclasses import replace

    others = [task for task in tasks if task.name != name]
    target = next((task for task in tasks if task.name == name), None)
    if target is None:
        raise KeyError(name)

    def works(deadline_minutes: int) -> bool:
        moved = replace(target, due=calendar.moment(deadline_minutes))
        return feasible(others + [moved], calendar)

    low = calendar.minutes(target.due)
    if works(low):
        return low
    if not works(limit):
        return None
    high = limit
    while low + 1 < high:
        middle = (low + high) // 2
        if works(middle):
            high = middle
        else:
            low = middle
    return high
