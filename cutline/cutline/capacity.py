"""The capacity calendar: when work can actually happen.

Working hours minus fixed appointments minus days off, expressed as disjoint free
intervals measured in whole minutes from the plan's ``now``.
"""

from __future__ import annotations

from bisect import bisect_right
from datetime import datetime, timedelta
from typing import Iterable, List, Optional, Sequence, Tuple

from .plan import Plan

Interval = Tuple[int, int]


def subtract(intervals: Sequence[Interval], holes: Sequence[Interval]) -> List[Interval]:
    """Remove ``holes`` from ``intervals``. Both may be unsorted or overlapping."""
    result = merge(intervals)
    for hole_start, hole_end in merge(holes):
        if hole_end <= hole_start:
            continue
        updated: List[Interval] = []
        for start, end in result:
            if hole_end <= start or hole_start >= end:
                updated.append((start, end))
                continue
            if start < hole_start:
                updated.append((start, hole_start))
            if hole_end < end:
                updated.append((hole_end, end))
        result = updated
    return result


def merge(intervals: Iterable[Interval]) -> List[Interval]:
    """Sort and merge overlapping or touching intervals, dropping empty ones."""
    ordered = sorted((start, end) for start, end in intervals if end > start)
    merged: List[Interval] = []
    for start, end in ordered:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


class Calendar:
    """Free time as disjoint intervals, with capacity queries over any window."""

    def __init__(self, plan: Plan, horizon: Optional[datetime] = None) -> None:
        self.origin = plan.now
        self.horizon = horizon if horizon is not None else plan.horizon()
        self.free: Tuple[Interval, ...] = tuple(self._build(plan))
        self._starts = [start for start, _ in self.free]
        self._prefix: List[int] = [0]
        for start, end in self.free:
            self._prefix.append(self._prefix[-1] + (end - start))

    # ---------------------------------------------------------------- building

    def _build(self, plan: Plan) -> List[Interval]:
        if self.horizon <= self.origin or not plan.hours:
            return []
        windows: List[Interval] = []
        day = self.origin.date()
        last_day = self.horizon.date()
        while day <= last_day:
            if day not in plan.off:
                for start, end in plan.hours.get(day.weekday(), ()):
                    window_start = datetime.combine(day, start)
                    window_end = datetime.combine(day, end)
                    clipped_start = max(window_start, self.origin)
                    clipped_end = min(window_end, self.horizon)
                    if clipped_end > clipped_start:
                        windows.append(
                            (self.minutes(clipped_start), self.minutes(clipped_end))
                        )
            day += timedelta(days=1)
        holes = [
            (self.minutes(block.start), self.minutes(block.end)) for block in plan.busy
        ]
        return subtract(windows, holes)

    # ----------------------------------------------------------- time handling

    def minutes(self, moment: datetime) -> int:
        """Whole minutes from the plan's ``now`` to ``moment`` (may be negative)."""
        delta = moment - self.origin
        return int(delta.total_seconds() // 60)

    def moment(self, minutes: int) -> datetime:
        return self.origin + timedelta(minutes=minutes)

    # --------------------------------------------------------------- capacity

    def up_to(self, point: int) -> int:
        """Free minutes between the origin and ``point``."""
        if point <= 0 or not self.free:
            return 0
        index = bisect_right(self._starts, point) - 1
        if index < 0:
            return 0
        total = self._prefix[index]
        start, end = self.free[index]
        total += max(0, min(point, end) - start)
        return total

    def capacity(self, start: int, end: int) -> int:
        """Free minutes inside ``[start, end)``."""
        if end <= start:
            return 0
        return self.up_to(end) - self.up_to(start)

    def total(self) -> int:
        return self._prefix[-1] if self._prefix else 0

    def first_free_after(self, point: int) -> Optional[int]:
        """The earliest free minute at or after ``point``."""
        for start, end in self.free:
            if end > point:
                return max(start, point)
        return None

    def advance(self, point: int, minutes: int) -> Optional[int]:
        """The moment by which ``minutes`` of free time have elapsed after ``point``.

        Returns ``None`` when the calendar runs out of free time first.
        """
        if minutes <= 0:
            return point
        remaining = minutes
        for start, end in self.free:
            if end <= point:
                continue
            usable = end - max(start, point)
            if usable >= remaining:
                return max(start, point) + remaining
            remaining -= usable
        return None
