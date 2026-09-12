"""The plan model and its plain-text parser.

A plan is one text file describing when you can work and what you have committed to:

    now: 2026-09-14 09:00

    hours:
      mon-fri: 09:00-12:30, 13:30-17:30
      sat: 10:00-13:00

    off: 2026-09-16

    busy:
      2026-09-14 11:00-12:00  standup
      2026-09-15 14:00-15:30  dentist

    tasks:
      spec draft        4h    due 2026-09-15 17:00  weight 3
      migration script  6h30m due 2026-09-17 12:00  required
      code review       45m   due 2026-09-14 17:00  earliest 2026-09-14 13:30

All times are naive local times. Durations are whole minutes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from typing import Dict, FrozenSet, List, Optional, Sequence, Tuple

WEEKDAYS = {
    "mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6,
}
WEEKDAY_NAMES = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")

_DURATION_RE = re.compile(
    r"^(?:(?P<hours>\d+(?:\.\d+)?)h)?(?:(?P<minutes>\d+(?:\.\d+)?)m)?$", re.IGNORECASE
)
_TIME_RE = re.compile(r"^(?P<hour>\d{1,2}):(?P<minute>\d{2})$")
_DATE_RE = re.compile(r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})$")
_RANGE_RE = re.compile(r"^(?P<start>\d{1,2}:\d{2})\s*-\s*(?P<end>\d{1,2}:\d{2})$")

SECTIONS = ("hours", "busy", "tasks")
SCALARS = ("now", "off")


class PlanError(Exception):
    """Raised when a plan file cannot be read as a plan.

    Carries every problem found, each with its line number, so one run reports all
    of them instead of one per attempt.
    """

    def __init__(self, problems: Sequence[str]) -> None:
        self.problems = list(problems)
        super().__init__("; ".join(self.problems))


@dataclass(frozen=True)
class Task:
    name: str
    estimate: int
    due: datetime
    earliest: Optional[datetime] = None
    weight: float = 1.0
    required: bool = False
    line: int = 0

    def release(self, now: datetime) -> datetime:
        return max(self.earliest, now) if self.earliest is not None else now


@dataclass(frozen=True)
class Busy:
    start: datetime
    end: datetime
    label: str = ""
    line: int = 0


@dataclass(frozen=True)
class Plan:
    now: datetime
    hours: Dict[int, Tuple[Tuple[time, time], ...]] = field(default_factory=dict)
    busy: Tuple[Busy, ...] = ()
    off: FrozenSet[date] = frozenset()
    tasks: Tuple[Task, ...] = ()

    def horizon(self) -> datetime:
        """Last moment any task is due, or ``now`` when there are no tasks."""
        if not self.tasks:
            return self.now
        return max(task.due for task in self.tasks)

    def task(self, name: str) -> Task:
        for task in self.tasks:
            if task.name == name:
                return task
        raise KeyError(name)

    def with_tasks(self, tasks: Sequence[Task]) -> "Plan":
        return Plan(self.now, dict(self.hours), self.busy, self.off, tuple(tasks))

    def weekly_minutes(self) -> int:
        total = 0
        for windows in self.hours.values():
            for start, end in windows:
                total += _minutes_of(end) - _minutes_of(start)
        return total


def _minutes_of(value: time) -> int:
    return value.hour * 60 + value.minute


def parse_duration(text: str) -> int:
    """Parse ``4h``, ``45m``, ``6h30m`` or ``1.5h`` into whole minutes."""
    match = _DURATION_RE.match(text.strip())
    if match is None or not any(match.group(name) for name in ("hours", "minutes")):
        raise ValueError(f"{text!r} is not a duration such as 90m, 2h or 1h30m")
    total = 0.0
    if match.group("hours"):
        total += float(match.group("hours")) * 60
    if match.group("minutes"):
        total += float(match.group("minutes"))
    minutes = int(round(total))
    if minutes <= 0:
        raise ValueError(f"{text!r} is not a positive duration")
    if abs(total - minutes) > 1e-9:
        raise ValueError(f"{text!r} is not a whole number of minutes")
    return minutes


def format_duration(minutes: int) -> str:
    """Render minutes as ``6h30m``, ``45m`` or ``2h``."""
    sign = "-" if minutes < 0 else ""
    minutes = abs(int(minutes))
    hours, rest = divmod(minutes, 60)
    if hours and rest:
        return f"{sign}{hours}h{rest}m"
    if hours:
        return f"{sign}{hours}h"
    return f"{sign}{rest}m"


def format_delay(minutes: int) -> str:
    """Render a wall-clock shift as days and hours, for deadline suggestions."""
    minutes = int(minutes)
    if minutes < 0:
        return "earlier"
    days, rest = divmod(minutes, 24 * 60)
    hours, mins = divmod(rest, 60)
    parts = []
    if days:
        parts.append(f"{days} day" + ("s" if days != 1 else ""))
    if hours:
        parts.append(f"{hours}h")
    if mins and not days:
        parts.append(f"{mins}m")
    return " ".join(parts) if parts else "0m"


def parse_clock(text: str) -> time:
    match = _TIME_RE.match(text.strip())
    if match is None:
        raise ValueError(f"{text!r} is not a time of day such as 09:30")
    hour, minute = int(match.group("hour")), int(match.group("minute"))
    if hour > 23 or minute > 59:
        raise ValueError(f"{text!r} is not a valid time of day")
    return time(hour, minute)


def parse_date(text: str) -> date:
    match = _DATE_RE.match(text.strip())
    if match is None:
        raise ValueError(f"{text!r} is not a date such as 2026-09-14")
    try:
        return date(
            int(match.group("year")), int(match.group("month")), int(match.group("day"))
        )
    except ValueError as exc:
        raise ValueError(f"{text!r} is not a valid date: {exc}") from exc


def parse_moment(tokens: Sequence[str], *, end_of_day: bool = False) -> Tuple[datetime, int]:
    """Parse a date, optionally followed by a time. Returns the value and tokens used.

    A bare date means the end of that day (23:59) when ``end_of_day`` is set, which is
    what a deadline written as a plain date means, and midnight otherwise.
    """
    if not tokens:
        raise ValueError("expected a date")
    day = parse_date(tokens[0])
    if len(tokens) > 1 and _TIME_RE.match(tokens[1]):
        clock = parse_clock(tokens[1])
        return datetime.combine(day, clock), 2
    if end_of_day:
        return datetime.combine(day, time(23, 59)), 1
    return datetime.combine(day, time(0, 0)), 1


def parse_weekday_spec(text: str) -> List[int]:
    """Parse ``mon``, ``mon-fri`` or ``mon,wed,fri`` into weekday numbers."""
    days: List[int] = []
    for part in text.split(","):
        part = part.strip().lower()
        if not part:
            continue
        if "-" in part:
            first, _, last = part.partition("-")
            first, last = first.strip(), last.strip()
            if first not in WEEKDAYS or last not in WEEKDAYS:
                raise ValueError(f"{part!r} is not a weekday range such as mon-fri")
            start, stop = WEEKDAYS[first], WEEKDAYS[last]
            span = (
                range(start, stop + 1)
                if start <= stop
                else list(range(start, 7)) + list(range(0, stop + 1))
            )
            days.extend(span)
        else:
            if part not in WEEKDAYS:
                raise ValueError(
                    f"{part!r} is not a weekday; use one of {', '.join(WEEKDAY_NAMES)}"
                )
            days.append(WEEKDAYS[part])
    if not days:
        raise ValueError("no weekdays given")
    return sorted(set(days))


class _Parser:
    def __init__(self, text: str) -> None:
        self.text = text
        self.problems: List[str] = []
        self.now: Optional[datetime] = None
        self.hours: Dict[int, List[Tuple[time, time]]] = {}
        self.busy: List[Busy] = []
        self.off: List[date] = []
        self.tasks: List[Task] = []

    def fail(self, line: int, message: str) -> None:
        self.problems.append(f"line {line}: {message}")

    def parse(self) -> Plan:
        section: Optional[str] = None
        for number, raw in enumerate(self.text.splitlines(), start=1):
            line = raw.split("#", 1)[0].rstrip()
            if not line.strip():
                continue
            indented = line[0].isspace()
            stripped = line.strip()

            if not indented:
                key, separator, value = stripped.partition(":")
                key = key.strip().lower()
                if not separator:
                    self.fail(number, f"expected a section or 'key: value', got {stripped!r}")
                    continue
                if key in SECTIONS:
                    section = key
                    if value.strip():
                        self.entry(key, value.strip(), number)
                    continue
                section = None
                if key in SCALARS:
                    self.scalar(key, value.strip(), number)
                else:
                    self.fail(
                        number,
                        f"unknown setting {key!r}; expected one of "
                        f"{', '.join(sorted(SCALARS + SECTIONS))}",
                    )
                continue

            if section is None:
                self.fail(number, f"indented line outside any section: {stripped!r}")
                continue
            self.entry(section, stripped, number)

        if self.now is None:
            self.problems.append("missing required setting 'now: YYYY-MM-DD HH:MM'")
        if not self.hours:
            self.problems.append("missing required section 'hours:'")

        if self.problems:
            raise PlanError(self.problems)

        assert self.now is not None
        plan = Plan(
            now=self.now,
            hours={day: tuple(sorted(windows)) for day, windows in self.hours.items()},
            busy=tuple(sorted(self.busy, key=lambda item: (item.start, item.end))),
            off=frozenset(self.off),
            tasks=tuple(self.tasks),
        )
        self.validate(plan)
        if self.problems:
            raise PlanError(self.problems)
        return plan

    # ------------------------------------------------------------------ pieces

    def scalar(self, key: str, value: str, number: int) -> None:
        if key == "now":
            if not value:
                self.fail(number, "'now' needs a date and time, such as 2026-09-14 09:00")
                return
            try:
                moment, _ = parse_moment(value.split())
            except ValueError as exc:
                self.fail(number, str(exc))
                return
            self.now = moment
        elif key == "off":
            for part in value.split(","):
                part = part.strip()
                if not part:
                    continue
                try:
                    self.off.append(parse_date(part))
                except ValueError as exc:
                    self.fail(number, str(exc))

    def entry(self, section: str, text: str, number: int) -> None:
        if section == "hours":
            self.hours_entry(text, number)
        elif section == "busy":
            self.busy_entry(text, number)
        elif section == "tasks":
            self.task_entry(text, number)

    def hours_entry(self, text: str, number: int) -> None:
        days_text, separator, ranges_text = text.partition(":")
        if not separator:
            self.fail(number, f"expected 'weekdays: HH:MM-HH:MM', got {text!r}")
            return
        try:
            days = parse_weekday_spec(days_text)
        except ValueError as exc:
            self.fail(number, str(exc))
            return
        windows: List[Tuple[time, time]] = []
        for part in ranges_text.split(","):
            part = part.strip()
            if not part:
                continue
            match = _RANGE_RE.match(part)
            if match is None:
                self.fail(number, f"{part!r} is not a time range such as 09:00-12:30")
                continue
            try:
                start = parse_clock(match.group("start"))
                end = parse_clock(match.group("end"))
            except ValueError as exc:
                self.fail(number, str(exc))
                continue
            if _minutes_of(end) <= _minutes_of(start):
                self.fail(number, f"{part!r} ends before it starts")
                continue
            windows.append((start, end))
        if not windows:
            self.fail(number, f"no usable time ranges in {text!r}")
            return
        for day in days:
            existing = self.hours.setdefault(day, [])
            for start, end in windows:
                for other_start, other_end in existing:
                    if _minutes_of(start) < _minutes_of(other_end) and _minutes_of(
                        other_start
                    ) < _minutes_of(end):
                        self.fail(
                            number,
                            f"working hours for {WEEKDAY_NAMES[day]} overlap "
                            f"{other_start:%H:%M}-{other_end:%H:%M}",
                        )
                        break
                else:
                    existing.append((start, end))

    def busy_entry(self, text: str, number: int) -> None:
        tokens = text.split()
        if len(tokens) < 2:
            self.fail(
                number,
                f"expected 'YYYY-MM-DD HH:MM-HH:MM label', got {text!r}",
            )
            return
        try:
            day = parse_date(tokens[0])
        except ValueError as exc:
            self.fail(number, str(exc))
            return
        match = _RANGE_RE.match(tokens[1])
        if match is None:
            self.fail(number, f"{tokens[1]!r} is not a time range such as 11:00-12:00")
            return
        try:
            start = parse_clock(match.group("start"))
            end = parse_clock(match.group("end"))
        except ValueError as exc:
            self.fail(number, str(exc))
            return
        if _minutes_of(end) <= _minutes_of(start):
            self.fail(number, f"busy block {tokens[1]!r} ends before it starts")
            return
        self.busy.append(
            Busy(
                start=datetime.combine(day, start),
                end=datetime.combine(day, end),
                label=" ".join(tokens[2:]),
                line=number,
            )
        )

    def task_entry(self, text: str, number: int) -> None:
        tokens = text.split()
        estimate_index = next(
            (
                index
                for index, token in enumerate(tokens)
                if _DURATION_RE.match(token) and any(char.isdigit() for char in token)
            ),
            None,
        )
        if estimate_index is None or estimate_index == 0:
            self.fail(
                number,
                f"expected 'name DURATION due DATE [TIME] [earliest ...] [weight N] "
                f"[required]', got {text!r}",
            )
            return
        name = " ".join(tokens[:estimate_index])
        try:
            estimate = parse_duration(tokens[estimate_index])
        except ValueError as exc:
            self.fail(number, str(exc))
            return

        due: Optional[datetime] = None
        earliest: Optional[datetime] = None
        weight = 1.0
        required = False
        index = estimate_index + 1
        while index < len(tokens):
            keyword = tokens[index].lower()
            rest = tokens[index + 1:]
            if keyword in ("due", "earliest"):
                try:
                    moment, used = parse_moment(rest, end_of_day=keyword == "due")
                except ValueError as exc:
                    self.fail(number, f"{keyword}: {exc}")
                    return
                if keyword == "due":
                    due = moment
                else:
                    earliest = moment
                index += 1 + used
            elif keyword == "weight":
                if not rest:
                    self.fail(number, "weight needs a number")
                    return
                try:
                    weight = float(rest[0])
                except ValueError:
                    self.fail(number, f"{rest[0]!r} is not a number for weight")
                    return
                if weight <= 0:
                    self.fail(number, "weight must be greater than zero")
                    return
                index += 2
            elif keyword == "required":
                required = True
                index += 1
            else:
                self.fail(
                    number,
                    f"unexpected {tokens[index]!r} in task line; expected due, "
                    f"earliest, weight or required",
                )
                return

        if due is None:
            self.fail(number, f"task {name!r} has no 'due' date")
            return
        self.tasks.append(
            Task(
                name=name,
                estimate=estimate,
                due=due,
                earliest=earliest,
                weight=weight,
                required=required,
                line=number,
            )
        )

    # -------------------------------------------------------------- validation

    def validate(self, plan: Plan) -> None:
        seen: Dict[str, int] = {}
        for task in plan.tasks:
            if task.name in seen:
                self.fail(
                    task.line,
                    f"task name {task.name!r} already used on line {seen[task.name]}",
                )
            seen[task.name] = task.line
            if task.due <= plan.now:
                self.fail(
                    task.line,
                    f"task {task.name!r} is due at or before 'now' "
                    f"({task.due:%Y-%m-%d %H:%M} <= {plan.now:%Y-%m-%d %H:%M})",
                )
            if task.earliest is not None and task.earliest >= task.due:
                self.fail(
                    task.line,
                    f"task {task.name!r} cannot start after its deadline",
                )
        for block in plan.busy:
            if block.end <= plan.now:
                continue
        horizon = plan.horizon()
        if (horizon - plan.now) > timedelta(days=3650):
            self.problems.append("deadlines more than ten years out are not supported")


def parse_plan(text: str) -> Plan:
    """Parse plan text, raising :class:`PlanError` listing every problem found."""
    return _Parser(text).parse()


def load_plan(path: str) -> Plan:
    """Read and parse a plan file."""
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except FileNotFoundError:
        raise PlanError([f"no such plan file: {path}"]) from None
    except IsADirectoryError:
        raise PlanError([f"{path} is a directory, not a plan file"]) from None
    except UnicodeDecodeError as exc:
        raise PlanError([f"{path} is not valid UTF-8: {exc.reason}"]) from None
    except OSError as exc:
        raise PlanError([f"cannot read {path}: {exc.strerror}"]) from None
    return parse_plan(text)
