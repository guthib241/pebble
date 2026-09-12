"""Tests for interval arithmetic and the capacity calendar."""

from __future__ import annotations

import unittest
from datetime import datetime, time, timedelta

from cutline.capacity import Calendar, merge, subtract
from cutline.plan import Busy
from tests.support import MONDAY, at, plan_of, task


class IntervalTest(unittest.TestCase):
    def test_merge_sorts_and_joins(self):
        self.assertEqual(merge([(5, 8), (0, 3), (2, 6)]), [(0, 8)])
        self.assertEqual(merge([(0, 3), (3, 5)]), [(0, 5)])
        self.assertEqual(merge([(0, 3), (4, 5)]), [(0, 3), (4, 5)])

    def test_merge_drops_empty_intervals(self):
        self.assertEqual(merge([(5, 5), (1, 0)]), [])

    def test_subtract_middle_start_and_end(self):
        self.assertEqual(subtract([(0, 10)], [(4, 6)]), [(0, 4), (6, 10)])
        self.assertEqual(subtract([(0, 10)], [(0, 4)]), [(4, 10)])
        self.assertEqual(subtract([(0, 10)], [(8, 12)]), [(0, 8)])

    def test_subtract_whole_and_disjoint(self):
        self.assertEqual(subtract([(0, 10)], [(0, 10)]), [])
        self.assertEqual(subtract([(0, 10)], [(20, 30)]), [(0, 10)])

    def test_subtract_multiple_holes(self):
        self.assertEqual(
            subtract([(0, 20)], [(2, 4), (10, 12), (18, 19)]),
            [(0, 2), (4, 10), (12, 18), (19, 20)],
        )

    def test_subtract_empty_hole_is_ignored(self):
        self.assertEqual(subtract([(0, 10)], [(5, 5)]), [(0, 10)])


class CalendarTest(unittest.TestCase):
    def test_office_hours_produce_two_blocks_a_day(self):
        plan = plan_of([task("a", 30, at(0, 17))])
        calendar = Calendar(plan, MONDAY + timedelta(days=1))
        self.assertEqual(len(calendar.free), 2)
        self.assertEqual(calendar.total(), 450)

    def test_capacity_starts_at_now_not_at_midnight(self):
        plan = plan_of([task("a", 30, at(0, 17))], now=at(0, 11))
        calendar = Calendar(plan, at(0, 17, 30))
        # 11:00-12:30 and 13:30-17:30 is 5h30m.
        self.assertEqual(calendar.total(), 330)

    def test_busy_blocks_are_removed(self):
        plan = plan_of(
            [task("a", 30, at(0, 17, 30))],
            busy=[Busy(start=at(0, 11), end=at(0, 12), label="standup")],
        )
        calendar = Calendar(plan, at(0, 17, 30))
        self.assertEqual(calendar.total(), 450 - 60)
        self.assertEqual(len(calendar.free), 3)

    def test_busy_block_outside_working_hours_changes_nothing(self):
        plan = plan_of(
            [task("a", 30, at(0, 17, 30))],
            busy=[Busy(start=at(0, 19), end=at(0, 20), label="dinner")],
        )
        calendar = Calendar(plan, at(0, 17, 30))
        self.assertEqual(calendar.total(), 450)

    def test_days_off_are_removed(self):
        plan = plan_of([task("a", 30, at(2, 17, 30))])
        with_off = plan_of([task("a", 30, at(2, 17, 30))], off={at(1, 0).date()})
        horizon = at(2, 17, 30)
        self.assertEqual(Calendar(plan, horizon).total(), 3 * 450)
        self.assertEqual(Calendar(with_off, horizon).total(), 2 * 450)

    def test_weekend_without_hours_is_unavailable(self):
        plan = plan_of([task("a", 30, at(6, 17, 30))])
        calendar = Calendar(plan, at(6, 17, 30))
        # Monday to Friday only: five working days.
        self.assertEqual(calendar.total(), 5 * 450)

    def test_capacity_queries(self):
        plan = plan_of([task("a", 30, at(0, 17, 30))])
        calendar = Calendar(plan, at(1, 17, 30))
        start = calendar.minutes(MONDAY)
        noon = calendar.minutes(at(0, 12))
        self.assertEqual(calendar.capacity(start, noon), 180)
        self.assertEqual(calendar.capacity(noon, noon), 0)
        self.assertEqual(calendar.capacity(noon, start), 0)
        self.assertEqual(
            calendar.capacity(start, calendar.minutes(at(0, 13))), 210
        )
        self.assertEqual(calendar.up_to(-10), 0)

    def test_capacity_over_the_whole_span_matches_total(self):
        plan = plan_of([task("a", 30, at(3, 17, 30))])
        calendar = Calendar(plan, at(3, 17, 30))
        self.assertEqual(
            calendar.capacity(0, calendar.minutes(at(3, 17, 30))), calendar.total()
        )

    def test_moment_and_minutes_round_trip(self):
        plan = plan_of([task("a", 30, at(0, 17))])
        calendar = Calendar(plan, at(0, 17, 30))
        for offset in (0, 1, 60, 1440):
            self.assertEqual(calendar.minutes(calendar.moment(offset)), offset)

    def test_first_free_after(self):
        plan = plan_of([task("a", 30, at(1, 17))])
        calendar = Calendar(plan, at(1, 17, 30))
        lunch = calendar.minutes(at(0, 13))
        self.assertEqual(
            calendar.moment(calendar.first_free_after(lunch)), at(0, 13, 30)
        )
        self.assertEqual(calendar.first_free_after(calendar.minutes(at(9, 0))), None)

    def test_advance_skips_unavailable_time(self):
        plan = plan_of([task("a", 30, at(1, 17))])
        calendar = Calendar(plan, at(1, 17, 30))
        # Four hours of work from Monday 09:00 lands after the lunch break.
        self.assertEqual(calendar.moment(calendar.advance(0, 240)), at(0, 14))
        self.assertEqual(calendar.advance(0, 0), 0)
        self.assertIsNone(calendar.advance(0, 100 * 60))

    def test_empty_calendar_when_the_horizon_is_now(self):
        plan = plan_of([])
        calendar = Calendar(plan, MONDAY)
        self.assertEqual(calendar.free, ())
        self.assertEqual(calendar.total(), 0)
        self.assertEqual(calendar.capacity(0, 1000), 0)
        self.assertIsNone(calendar.first_free_after(0))

    def test_plan_without_working_hours_has_no_capacity(self):
        plan = plan_of([task("a", 30, at(0, 17))], hours={})
        calendar = Calendar(plan, at(0, 17))
        self.assertEqual(calendar.total(), 0)

    def test_hours_spanning_a_single_minute(self):
        plan = plan_of(
            [task("a", 1, at(0, 10))],
            hours={0: ((time(9, 0), time(9, 1)),)},
        )
        calendar = Calendar(plan, at(0, 10))
        self.assertEqual(calendar.total(), 1)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
