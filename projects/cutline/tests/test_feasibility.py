"""Tests for the two feasibility methods, the certificate, slack and deferrals."""

from __future__ import annotations

import random
import unittest
from dataclasses import replace
from datetime import timedelta

from cutline.feasibility import (
    earliest_feasible_deadline,
    edf_schedule,
    feasible,
    slack_by_deadline,
    violated_windows,
    worst_window,
)
from cutline.plan import Task
from tests.support import (
    MONDAY,
    at,
    calendar_for,
    plan_of,
    random_plan,
    schedule_is_valid,
    task,
)


class EdfScheduleTest(unittest.TestCase):
    def test_empty_plan(self):
        plan = plan_of([])
        schedule = edf_schedule(plan.tasks, calendar_for(plan))
        self.assertEqual(schedule.blocks, ())
        self.assertTrue(schedule.feasible)

    def test_single_task_is_placed_at_the_first_free_minute(self):
        plan = plan_of([task("write", 60, at(0, 17))])
        calendar = calendar_for(plan)
        schedule = edf_schedule(plan.tasks, calendar)
        self.assertTrue(schedule.feasible)
        self.assertEqual(len(schedule.blocks), 1)
        block = schedule.blocks[0]
        self.assertEqual(calendar.moment(block.start), MONDAY)
        self.assertEqual(calendar.moment(block.end), MONDAY + timedelta(minutes=60))

    def test_work_splits_across_the_lunch_break(self):
        plan = plan_of([task("long", 5 * 60, at(0, 17, 30))])
        calendar = calendar_for(plan)
        schedule = edf_schedule(plan.tasks, calendar)
        self.assertTrue(schedule.feasible)
        self.assertEqual(len(schedule.blocks), 2)
        self.assertEqual(calendar.moment(schedule.blocks[0].end).hour, 12)
        self.assertEqual(calendar.moment(schedule.blocks[1].start).hour, 13)
        self.assertEqual(sum(block.minutes for block in schedule.blocks), 5 * 60)

    def test_earlier_deadline_goes_first(self):
        plan = plan_of(
            [
                task("later", 60, at(1, 12)),
                task("sooner", 60, at(0, 11)),
            ]
        )
        schedule = edf_schedule(plan.tasks, calendar_for(plan))
        self.assertEqual(schedule.blocks[0].task, "sooner")

    def test_release_time_is_respected_and_preempts(self):
        plan = plan_of(
            [
                task("background", 5 * 60, at(1, 17)),
                task("urgent", 60, at(0, 15), earliest=at(0, 13, 30)),
            ]
        )
        calendar = calendar_for(plan)
        schedule = edf_schedule(plan.tasks, calendar)
        self.assertTrue(schedule.feasible)
        urgent = [block for block in schedule.blocks if block.task == "urgent"]
        self.assertEqual(len(urgent), 1)
        self.assertEqual(calendar.moment(urgent[0].start).hour, 13)
        self.assertEqual(calendar.moment(urgent[0].start).minute, 30)

    def test_late_task_is_reported_with_its_shortfall(self):
        plan = plan_of([task("huge", 10 * 60, at(0, 17, 30))])
        schedule = edf_schedule(plan.tasks, calendar_for(plan))
        self.assertEqual(schedule.late, ("huge",))
        # Monday 09:00-12:30 and 13:30-17:30 is 7h30m of capacity.
        self.assertEqual(schedule.shortfall["huge"], 10 * 60 - 450)

    def test_busy_blocks_remove_capacity(self):
        from cutline.plan import Busy

        plan = plan_of(
            [task("work", 450, at(0, 17, 30))],
            busy=[Busy(start=at(0, 11), end=at(0, 12), label="standup")],
        )
        schedule = edf_schedule(plan.tasks, calendar_for(plan))
        self.assertEqual(schedule.late, ("work",))
        self.assertEqual(schedule.shortfall["work"], 60)

    def test_day_off_removes_a_whole_day(self):
        plan = plan_of(
            [task("work", 450, at(1, 17, 30))],
            off={at(0, 0).date()},
        )
        schedule = edf_schedule(plan.tasks, calendar_for(plan))
        self.assertTrue(schedule.feasible)
        for block in schedule.blocks:
            self.assertNotEqual(block.start, 0)


class WindowCertificateTest(unittest.TestCase):
    def test_no_windows_when_everything_fits(self):
        plan = plan_of([task("small", 30, at(0, 17))])
        self.assertEqual(violated_windows(plan.tasks, calendar_for(plan)), [])
        self.assertTrue(feasible(plan.tasks, calendar_for(plan)))

    def test_certificate_names_the_deficit_and_the_tasks(self):
        plan = plan_of(
            [
                task("a", 4 * 60, at(0, 17, 30)),
                task("b", 4 * 60, at(0, 17, 30)),
            ]
        )
        calendar = calendar_for(plan)
        window = worst_window(plan.tasks, calendar)
        self.assertIsNotNone(window)
        assert window is not None
        self.assertEqual(window.work, 8 * 60)
        self.assertEqual(window.capacity, 450)
        self.assertEqual(window.deficit, 8 * 60 - 450)
        self.assertEqual(window.tasks, ("a", "b"))
        self.assertEqual(calendar.moment(window.start), MONDAY)
        self.assertEqual(calendar.moment(window.end), at(0, 17, 30))

    def test_release_time_narrows_the_window(self):
        plan = plan_of(
            [
                task("morning", 60, at(0, 17)),
                task("afternoon", 5 * 60, at(0, 17, 30), earliest=at(0, 13, 30)),
            ]
        )
        calendar = calendar_for(plan)
        window = worst_window(plan.tasks, calendar)
        assert window is not None
        # The afternoon task alone cannot fit between 13:30 and 17:30.
        self.assertEqual(window.tasks, ("afternoon",))
        self.assertEqual(calendar.moment(window.start), at(0, 13, 30))
        self.assertEqual(window.capacity, 4 * 60)

    def test_windows_are_ordered_by_severity(self):
        plan = plan_of(
            [
                task("a", 8 * 60, at(0, 17, 30)),
                task("b", 60, at(1, 17, 30)),
            ]
        )
        windows = violated_windows(plan.tasks, calendar_for(plan))
        self.assertTrue(windows)
        deficits = [window.deficit for window in windows]
        self.assertEqual(deficits, sorted(deficits, reverse=True))


class MethodsAgreeTest(unittest.TestCase):
    """The window condition and the EDF schedule must always give the same verdict."""

    def test_agreement_on_random_instances(self):
        rng = random.Random(20260912)
        both = {True: 0, False: 0}
        for index in range(400):
            plan = random_plan(rng, rng.randint(1, 7))
            calendar = calendar_for(plan)
            by_windows = feasible(plan.tasks, calendar)
            schedule = edf_schedule(plan.tasks, calendar)
            self.assertEqual(
                by_windows,
                schedule.feasible,
                f"instance {index} disagrees: windows={by_windows}, edf={schedule.feasible}",
            )
            both[by_windows] += 1
            valid, reason = schedule_is_valid(schedule, plan, calendar)
            self.assertTrue(valid, f"instance {index}: {reason}")
        # The generator must produce both verdicts, or the test proves nothing.
        self.assertGreater(both[True], 20, "no feasible instances were generated")
        self.assertGreater(both[False], 20, "no infeasible instances were generated")

    def test_schedule_validity_on_tight_instances(self):
        rng = random.Random(7)
        for _ in range(120):
            plan = random_plan(rng, rng.randint(2, 5))
            calendar = calendar_for(plan)
            schedule = edf_schedule(plan.tasks, calendar)
            valid, reason = schedule_is_valid(schedule, plan, calendar)
            self.assertTrue(valid, reason)


class SlackTest(unittest.TestCase):
    def test_slack_is_exactly_the_amount_that_still_fits(self):
        plan = plan_of(
            [
                task("a", 120, at(0, 17, 30)),
                task("b", 180, at(1, 17, 30)),
            ]
        )
        calendar = calendar_for(plan)
        for deadline, spare in slack_by_deadline(plan.tasks, calendar):
            extra = Task(name="extra", estimate=spare, due=calendar.moment(deadline))
            self.assertTrue(
                feasible(list(plan.tasks) + [extra], calendar),
                f"adding {spare} minutes due {calendar.moment(deadline)} should fit",
            )
            one_more = replace(extra, estimate=spare + 1)
            self.assertFalse(
                feasible(list(plan.tasks) + [one_more], calendar),
                f"adding {spare + 1} minutes due {calendar.moment(deadline)} should not fit",
            )

    def test_slack_property_on_random_feasible_instances(self):
        rng = random.Random(99)
        checked = 0
        for _ in range(200):
            plan = random_plan(rng, rng.randint(1, 5))
            calendar = calendar_for(plan)
            if not feasible(plan.tasks, calendar):
                continue
            checked += 1
            for deadline, spare in slack_by_deadline(plan.tasks, calendar):
                self.assertGreaterEqual(spare, 0)
                extra = Task(
                    name="extra", estimate=max(1, spare), due=calendar.moment(deadline)
                )
                expected = spare > 0
                self.assertEqual(
                    feasible(list(plan.tasks) + [extra], calendar),
                    expected,
                    f"slack {spare} at {calendar.moment(deadline)} is wrong",
                )
                too_much = replace(extra, estimate=spare + 1)
                self.assertFalse(feasible(list(plan.tasks) + [too_much], calendar))
        self.assertGreater(checked, 20)

    def test_slack_without_tasks_is_the_whole_calendar(self):
        plan = plan_of([])
        calendar = calendar_for(plan)
        slack = slack_by_deadline(plan.tasks, calendar)
        self.assertEqual(len(slack), 1)
        self.assertEqual(slack[0][1], calendar.capacity(0, slack[0][0]))


class DeferralTest(unittest.TestCase):
    def test_earliest_feasible_deadline_is_tight(self):
        plan = plan_of(
            [
                task("keep", 6 * 60, at(0, 17, 30)),
                task("move", 4 * 60, at(0, 17, 30)),
            ]
        )
        calendar = calendar_for(plan)
        limit = calendar.minutes(plan.horizon() + timedelta(days=20))
        found = earliest_feasible_deadline(plan.tasks, calendar, "move", limit)
        self.assertIsNotNone(found)
        assert found is not None
        moved = [
            replace(item, due=calendar.moment(found)) if item.name == "move" else item
            for item in plan.tasks
        ]
        self.assertTrue(feasible(moved, calendar))
        earlier = [
            replace(item, due=calendar.moment(found - 1))
            if item.name == "move"
            else item
            for item in plan.tasks
        ]
        self.assertFalse(feasible(earlier, calendar))

    def test_no_deadline_helps_when_another_task_is_the_problem(self):
        plan = plan_of(
            [
                task("impossible", 40 * 60, at(0, 17, 30)),
                task("move", 60, at(0, 17, 30)),
            ]
        )
        calendar = calendar_for(plan)
        limit = calendar.minutes(plan.horizon() + timedelta(days=10))
        self.assertIsNone(
            earliest_feasible_deadline(plan.tasks, calendar, "move", limit)
        )

    def test_unknown_task_name(self):
        plan = plan_of([task("a", 30, at(0, 17))])
        calendar = calendar_for(plan)
        with self.assertRaises(KeyError):
            earliest_feasible_deadline(plan.tasks, calendar, "missing", 1000)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
