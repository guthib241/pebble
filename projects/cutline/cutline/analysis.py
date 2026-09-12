"""Running the whole analysis: verdict, certificate, cut, deferrals, slack."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Sequence, Tuple

from .capacity import Calendar
from .cut import DEFAULT_NODE_BUDGET, Cut, deferrals, minimum_cut
from .feasibility import (
    Schedule,
    Window,
    edf_schedule,
    slack_by_deadline,
    violated_windows,
)
from .plan import Plan, Task

DEFAULT_DEFER_LIMIT_DAYS = 120


@dataclass(frozen=True)
class Analysis:
    plan: Plan
    calendar: Calendar
    source: str
    horizon: datetime
    capacity_minutes: int
    committed_minutes: int
    feasible: bool
    schedule: Schedule
    windows: Tuple[Window, ...]
    cut: Cut
    deferral: Dict[str, Optional[int]] = field(default_factory=dict)
    slack: Tuple[Tuple[int, int], ...] = ()
    slack_after_cut: Tuple[Tuple[int, int], ...] = ()
    methods_agree: bool = True
    added: Optional[Task] = None

    @property
    def worst(self) -> Optional[Window]:
        return self.windows[0] if self.windows else None

    def kept_tasks(self) -> List[Task]:
        return [task for task in self.plan.tasks if task.name not in self.cut.dropped]

    def moment(self, minutes: int) -> datetime:
        return self.calendar.moment(minutes)


def analyse(
    plan: Plan,
    source: str = "-",
    node_budget: int = DEFAULT_NODE_BUDGET,
    defer_limit_days: int = DEFAULT_DEFER_LIMIT_DAYS,
    added: Optional[Task] = None,
) -> Analysis:
    """Analyse a plan and return everything the reports need.

    The feasibility verdict is computed twice, by the window condition and by the
    earliest-deadline-first schedule. The two are independent and must agree;
    ``methods_agree`` records whether they did.
    """
    horizon = plan.horizon()
    calendar = Calendar(plan, horizon + timedelta(days=max(1, defer_limit_days)))
    horizon_minutes = calendar.minutes(horizon)

    windows = tuple(violated_windows(plan.tasks, calendar))
    schedule = edf_schedule(plan.tasks, calendar)
    feasible = not windows
    methods_agree = feasible == schedule.feasible

    cut = minimum_cut(plan.tasks, calendar, node_budget=node_budget)
    limit = calendar.minutes(horizon + timedelta(days=max(1, defer_limit_days)))
    deferral = (
        deferrals(plan.tasks, calendar, cut, limit) if cut.dropped and not cut.impossible else {}
    )

    kept = [task for task in plan.tasks if task.name not in cut.dropped]
    return Analysis(
        plan=plan,
        calendar=calendar,
        source=source,
        horizon=horizon,
        capacity_minutes=calendar.capacity(0, horizon_minutes),
        committed_minutes=sum(task.estimate for task in plan.tasks),
        feasible=feasible,
        schedule=schedule,
        windows=windows,
        cut=cut,
        deferral=deferral,
        slack=tuple(slack_by_deadline(plan.tasks, calendar)),
        slack_after_cut=tuple(slack_by_deadline(kept, calendar)),
        methods_agree=methods_agree,
        added=added,
    )


def tightest_slack(slack: Sequence[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    """The deadline with the least spare capacity."""
    if not slack:
        return None
    return min(slack, key=lambda item: (item[1], item[0]))
