"""cutline: decides whether your task list fits its deadlines, and what to cut."""

from __future__ import annotations

__version__ = "0.1.0"

from .analysis import Analysis, analyse
from .capacity import Calendar
from .cut import Cut, brute_force_cut, minimum_cut
from .feasibility import Schedule, Window, edf_schedule, feasible, violated_windows
from .plan import Plan, PlanError, Task, load_plan, parse_plan

__all__ = [
    "Analysis",
    "Calendar",
    "Cut",
    "Plan",
    "PlanError",
    "Schedule",
    "Task",
    "Window",
    "analyse",
    "brute_force_cut",
    "edf_schedule",
    "feasible",
    "load_plan",
    "minimum_cut",
    "parse_plan",
    "violated_windows",
    "__version__",
]
