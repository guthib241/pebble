"""Helpers shared by the tests: plan building and random instance generation."""

from __future__ import annotations

import random
from datetime import datetime, time, timedelta
from typing import List, Optional, Sequence, Tuple

from cutline.capacity import Calendar
from cutline.plan import Busy, Plan, Task

MONDAY = datetime(2026, 9, 14, 9, 0)  # a Monday, used as "now" in most tests
OFFICE_HOURS = {
    day: ((time(9, 0), time(12, 30)), (time(13, 30), time(17, 30)))
    for day in range(0, 5)
}


def plan_of(
    tasks: Sequence[Task],
    now: datetime = MONDAY,
    hours=None,
    busy: Sequence[Busy] = (),
    off=frozenset(),
) -> Plan:
    return Plan(
        now=now,
        hours=dict(OFFICE_HOURS if hours is None else hours),
        busy=tuple(busy),
        off=frozenset(off),
        tasks=tuple(tasks),
    )


def task(
    name: str,
    estimate_minutes: int,
    due: datetime,
    earliest: Optional[datetime] = None,
    weight: float = 1.0,
    required: bool = False,
) -> Task:
    return Task(
        name=name,
        estimate=estimate_minutes,
        due=due,
        earliest=earliest,
        weight=weight,
        required=required,
    )


def at(day_offset: int, hour: int, minute: int = 0, base: datetime = MONDAY) -> datetime:
    """A moment relative to the base date, e.g. ``at(0, 17)`` is Monday 17:00."""
    return datetime.combine(
        (base + timedelta(days=day_offset)).date(), time(hour, minute)
    )


def calendar_for(plan: Plan, extra_days: int = 30) -> Calendar:
    return Calendar(plan, plan.horizon() + timedelta(days=extra_days))


def random_plan(rng: random.Random, task_count: int) -> Plan:
    """A random but plausible plan, for property tests.

    Working hours, days off and appointments vary, and tasks get random estimates,
    deadlines, release times and weights, so instances land on both sides of the
    feasibility boundary.
    """
    hours = {}
    for day in range(0, 7):
        if rng.random() < 0.2:
            continue
        start_hour = rng.choice([8, 9, 10])
        windows = [(time(start_hour, 0), time(start_hour + rng.choice([3, 4]), 30))]
        if rng.random() < 0.7:
            windows.append((time(14, 0), time(rng.choice([16, 17, 18]), 0)))
        hours[day] = tuple(windows)

    busy: List[Busy] = []
    for offset in range(0, 6):
        if rng.random() < 0.4:
            hour = rng.choice([10, 11, 15])
            busy.append(
                Busy(
                    start=at(offset, hour),
                    end=at(offset, hour + 1),
                    label=f"meeting {offset}",
                )
            )

    off = frozenset(
        {at(offset, 0).date() for offset in range(0, 7) if rng.random() < 0.15}
    )

    tasks: List[Task] = []
    for index in range(task_count):
        day = rng.randint(0, 5)
        due = at(day, rng.choice([12, 17]), rng.choice([0, 30]))
        earliest = None
        if rng.random() < 0.3:
            candidates = [
                at(offset, hour)
                for offset in range(0, day + 1)
                for hour in (9, 13)
                if at(offset, hour) < due
            ]
            if candidates:
                earliest = rng.choice(candidates)
        tasks.append(
            Task(
                name=f"t{index}",
                estimate=rng.choice([30, 45, 60, 90, 120, 180, 240]),
                due=due,
                earliest=earliest,
                weight=rng.choice([0.5, 1.0, 1.0, 2.0, 3.0]),
                required=rng.random() < 0.12,
            )
        )
    return plan_of(tasks, hours=hours, busy=busy, off=off)


def schedule_is_valid(schedule, plan: Plan, calendar: Calendar) -> Tuple[bool, str]:
    """Check a schedule against the calendar and the tasks' own constraints."""
    free = calendar.free
    blocks = sorted(schedule.blocks, key=lambda block: block.start)
    for first, second in zip(blocks, blocks[1:]):
        if second.start < first.end:
            return False, f"blocks overlap: {first} and {second}"
    for block in blocks:
        if not any(start <= block.start and block.end <= end for start, end in free):
            return False, f"block outside free time: {block}"
        item = plan.task(block.task)
        release = max(0, calendar.minutes(item.release(plan.now)))
        if block.start < release:
            return False, f"block starts before the task is available: {block}"
        if block.end > calendar.minutes(item.due):
            return False, f"block ends after the deadline: {block}"
    done = {}
    for block in blocks:
        done[block.task] = done.get(block.task, 0) + block.minutes
    for item in plan.tasks:
        placed = done.get(item.name, 0)
        if item.name in schedule.late:
            if placed >= item.estimate:
                return False, f"{item.name} is marked late but fully placed"
        elif placed != item.estimate:
            return False, (
                f"{item.name} got {placed} minutes, estimate is {item.estimate}"
            )
    return True, ""
