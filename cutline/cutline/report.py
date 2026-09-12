"""Rendering an analysis as text or JSON."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Dict, List, Optional

from .analysis import Analysis, tightest_slack
from .plan import format_delay, format_duration


def _stamp(moment: datetime) -> str:
    return f"{moment:%a %Y-%m-%d %H:%M}"


def _short(moment: datetime) -> str:
    return f"{moment:%a %d %b %H:%M}"


def render_text(
    analysis: Analysis, show_schedule: bool = False, show_slack: bool = False
) -> str:
    lines: List[str] = []
    plan = analysis.plan
    lines.append(f"plan: {analysis.source}")
    lines.append(
        f"now: {_stamp(plan.now)}    last deadline: {_stamp(analysis.horizon)}"
    )
    lines.append(
        f"capacity until then: {format_duration(analysis.capacity_minutes)} free, "
        f"committed {format_duration(analysis.committed_minutes)} "
        f"across {len(plan.tasks)} task(s)"
    )
    if analysis.added is not None:
        lines.append(
            f"including the task added on the command line: "
            f"{analysis.added.name} ({format_duration(analysis.added.estimate)}, "
            f"due {_stamp(analysis.added.due)})"
        )
    lines.append("")

    if analysis.feasible:
        lines.append("VERDICT: fits")
        tight = tightest_slack(analysis.slack)
        if tight is not None:
            deadline, spare = tight
            lines.append(
                f"tightest deadline {_stamp(analysis.moment(deadline))} has "
                f"{format_duration(spare)} spare"
            )
    else:
        worst = analysis.worst
        assert worst is not None
        lines.append(
            f"VERDICT: does not fit, {format_duration(worst.deficit)} too much work"
        )
        lines.append("")
        lines.append("over-subscribed window")
        lines.append(
            f"  {_stamp(analysis.moment(worst.start))} "
            f"-> {_stamp(analysis.moment(worst.end))}"
        )
        lines.append(
            f"  capacity {format_duration(worst.capacity)}, "
            f"committed {format_duration(worst.work)}, "
            f"short {format_duration(worst.deficit)}"
        )
        lines.append(f"  tasks that must run inside it: {', '.join(worst.tasks)}")
        if len(analysis.windows) > 1:
            lines.append(
                f"  ({len(analysis.windows)} windows are over-subscribed; "
                f"the most severe is shown)"
            )
        lines.extend(_render_cut(analysis))

    if show_slack:
        lines.append("")
        lines.append("spare capacity for new work, by deadline")
        for deadline, spare in analysis.slack:
            lines.append(
                f"  by {_stamp(analysis.moment(deadline))}  {format_duration(spare)}"
            )

    if show_schedule:
        lines.append("")
        if analysis.schedule.blocks:
            lines.append("schedule (earliest deadline first)")
            for block in analysis.schedule.blocks:
                start = analysis.moment(block.start)
                end = analysis.moment(block.end)
                lines.append(
                    f"  {_short(start)}-{end:%H:%M}  "
                    f"{format_duration(block.minutes):>6}  {block.task}"
                )
        else:
            lines.append("schedule: nothing to place")
        if analysis.schedule.late:
            lines.append(
                "  unplaced work: "
                + ", ".join(
                    f"{name} ({format_duration(analysis.schedule.shortfall[name])})"
                    for name in analysis.schedule.late
                )
            )

    if not analysis.methods_agree:
        lines.append("")
        lines.append(
            "WARNING: the two feasibility methods disagree, which is a bug in cutline; "
            "please report the plan that produced this line"
        )

    return "\n".join(lines)


def _render_cut(analysis: Analysis) -> List[str]:
    cut = analysis.cut
    lines: List[str] = [""]
    if cut.impossible:
        lines.append(
            "no cut can fix this: the tasks marked required do not fit on their own"
        )
        required = [task.name for task in analysis.plan.tasks if task.required]
        lines.append(f"  required tasks: {', '.join(sorted(required))}")
        if cut.dropped:
            lines.append(
                f"  even after cutting everything else ({', '.join(cut.dropped)}) "
                f"the plan still does not fit"
            )
        return lines

    status = "proven minimal" if cut.proven_minimal else "NOT proven minimal, search budget spent"
    lines.append(
        f"cheapest cut ({status}, total weight {cut.weight:g}, "
        f"{cut.nodes} search node(s))"
    )
    by_name = {task.name: task for task in analysis.plan.tasks}
    for name in cut.dropped:
        task = by_name[name]
        lines.append(
            f"  cut {name}  {format_duration(task.estimate)}  "
            f"weight {task.weight:g}  due {_stamp(task.due)}"
        )
        when = analysis.deferral.get(name)
        if when is not None:
            moved = analysis.moment(when)
            delay = when - analysis.calendar.minutes(task.due)
            lines.append(
                f"      keep it by moving its deadline to {_stamp(moved)} "
                f"({format_delay(delay)} later)"
            )
        else:
            lines.append(
                "      moving its deadline does not help within the search limit"
            )
    tight = tightest_slack(analysis.slack_after_cut)
    if tight is not None:
        deadline, spare = tight
        lines.append(
            f"  after the cut the plan fits, tightest deadline "
            f"{_stamp(analysis.moment(deadline))} with {format_duration(spare)} spare"
        )
    return lines


def render_json(analysis: Analysis) -> str:
    plan = analysis.plan
    by_name = {task.name: task for task in plan.tasks}

    def moment(minutes: int) -> str:
        return analysis.moment(minutes).isoformat(timespec="minutes")

    payload: Dict[str, object] = {
        "source": analysis.source,
        "now": plan.now.isoformat(timespec="minutes"),
        "horizon": analysis.horizon.isoformat(timespec="minutes"),
        "capacity_minutes": analysis.capacity_minutes,
        "committed_minutes": analysis.committed_minutes,
        "task_count": len(plan.tasks),
        "feasible": analysis.feasible,
        "methods_agree": analysis.methods_agree,
        "tasks": [
            {
                "name": task.name,
                "estimate_minutes": task.estimate,
                "due": task.due.isoformat(timespec="minutes"),
                "earliest": (
                    task.earliest.isoformat(timespec="minutes")
                    if task.earliest is not None
                    else None
                ),
                "weight": task.weight,
                "required": task.required,
            }
            for task in plan.tasks
        ],
        "windows": [
            {
                "start": moment(window.start),
                "end": moment(window.end),
                "capacity_minutes": window.capacity,
                "work_minutes": window.work,
                "deficit_minutes": window.deficit,
                "tasks": list(window.tasks),
            }
            for window in analysis.windows
        ],
        "cut": {
            "dropped": list(analysis.cut.dropped),
            "weight": analysis.cut.weight,
            "proven_minimal": analysis.cut.proven_minimal,
            "budget_exhausted": analysis.cut.budget_exhausted,
            "search_nodes": analysis.cut.nodes,
            "impossible": analysis.cut.impossible,
            "deferrals": {
                name: (moment(value) if value is not None else None)
                for name, value in sorted(analysis.deferral.items())
            },
        },
        "slack": [
            {"deadline": moment(deadline), "spare_minutes": spare}
            for deadline, spare in analysis.slack
        ],
        "slack_after_cut": [
            {"deadline": moment(deadline), "spare_minutes": spare}
            for deadline, spare in analysis.slack_after_cut
        ],
        "schedule": [
            {
                "task": block.task,
                "start": moment(block.start),
                "end": moment(block.end),
                "minutes": block.minutes,
            }
            for block in analysis.schedule.blocks
        ],
        "unplaced": {
            name: analysis.schedule.shortfall[name] for name in analysis.schedule.late
        },
    }
    if analysis.added is not None:
        payload["added_task"] = analysis.added.name
    if by_name and analysis.cut.dropped:
        payload["cut"]["dropped_estimate_minutes"] = sum(  # type: ignore[index]
            by_name[name].estimate for name in analysis.cut.dropped
        )
    return json.dumps(payload, indent=2, sort_keys=True)
