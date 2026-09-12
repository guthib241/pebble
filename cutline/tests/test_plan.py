"""Tests for the plan parser, its error reporting and the duration helpers."""

from __future__ import annotations

import tempfile
import textwrap
import unittest
from datetime import date, datetime, time
from pathlib import Path

from cutline.plan import (
    PlanError,
    format_delay,
    format_duration,
    load_plan,
    parse_date,
    parse_duration,
    parse_moment,
    parse_plan,
    parse_weekday_spec,
)

GOOD = """\
# a week of work
now: 2026-09-14 09:00

hours:
  mon-fri: 09:00-12:30, 13:30-17:30
  sat: 10:00-13:00

off: 2026-09-16, 2026-12-25

busy:
  2026-09-14 11:00-12:00  standup with the team
  2026-09-15 14:00-15:30  dentist

tasks:
  spec draft        4h    due 2026-09-15 17:00  weight 3
  migration script  6h30m due 2026-09-17 12:00  required
  code review       45m   due 2026-09-14 17:00  earliest 2026-09-14 13:30
  slides            2h    due 2026-09-18
"""


class DurationTest(unittest.TestCase):
    def test_parse_forms(self):
        self.assertEqual(parse_duration("90m"), 90)
        self.assertEqual(parse_duration("1.1h"), 66)
        self.assertEqual(parse_duration("2h"), 120)
        self.assertEqual(parse_duration("6h30m"), 390)
        self.assertEqual(parse_duration("1.5h"), 90)
        self.assertEqual(parse_duration(" 45M "), 45)

    def test_rejects_bad_durations(self):
        for text in ("", "2", "2 hours", "0m", "-5m", "h", "1.51m", "1.0001h", "2d"):
            with self.assertRaises(ValueError, msg=text):
                parse_duration(text)

    def test_format_duration(self):
        self.assertEqual(format_duration(390), "6h30m")
        self.assertEqual(format_duration(120), "2h")
        self.assertEqual(format_duration(45), "45m")
        self.assertEqual(format_duration(0), "0m")
        self.assertEqual(format_duration(-90), "-1h30m")

    def test_format_delay(self):
        self.assertEqual(format_delay(30), "30m")
        self.assertEqual(format_delay(150), "2h 30m")
        self.assertEqual(format_delay(24 * 60), "1 day")
        self.assertEqual(format_delay(3 * 24 * 60 + 120), "3 days 2h")
        self.assertEqual(format_delay(0), "0m")


class TimeParsingTest(unittest.TestCase):
    def test_parse_date(self):
        self.assertEqual(parse_date("2026-09-14"), date(2026, 9, 14))

    def test_rejects_bad_dates(self):
        for text in ("14-09-2026", "2026-13-01", "2026-02-30", "not a date"):
            with self.assertRaises(ValueError, msg=text):
                parse_date(text)

    def test_parse_moment_with_and_without_time(self):
        self.assertEqual(
            parse_moment(["2026-09-14", "17:30"]), (datetime(2026, 9, 14, 17, 30), 2)
        )
        self.assertEqual(
            parse_moment(["2026-09-14"]), (datetime(2026, 9, 14, 0, 0), 1)
        )
        self.assertEqual(
            parse_moment(["2026-09-14"], end_of_day=True),
            (datetime(2026, 9, 14, 23, 59), 1),
        )

    def test_weekday_specs(self):
        self.assertEqual(parse_weekday_spec("mon"), [0])
        self.assertEqual(parse_weekday_spec("mon-fri"), [0, 1, 2, 3, 4])
        self.assertEqual(parse_weekday_spec("mon,wed,fri"), [0, 2, 4])
        self.assertEqual(parse_weekday_spec("sat-sun"), [5, 6])
        self.assertEqual(parse_weekday_spec("sat-mon"), [0, 5, 6])

    def test_bad_weekday_specs(self):
        for text in ("", "funday", "mon-funday", ","):
            with self.assertRaises(ValueError, msg=text):
                parse_weekday_spec(text)


class ParsePlanTest(unittest.TestCase):
    def setUp(self):
        self.plan = parse_plan(GOOD)

    def test_now(self):
        self.assertEqual(self.plan.now, datetime(2026, 9, 14, 9, 0))

    def test_hours(self):
        self.assertEqual(
            self.plan.hours[0], ((time(9, 0), time(12, 30)), (time(13, 30), time(17, 30)))
        )
        self.assertEqual(self.plan.hours[5], ((time(10, 0), time(13, 0)),))
        self.assertNotIn(6, self.plan.hours)
        self.assertEqual(self.plan.weekly_minutes(), 5 * 450 + 180)

    def test_off_days(self):
        self.assertEqual(self.plan.off, frozenset({date(2026, 9, 16), date(2026, 12, 25)}))

    def test_busy_blocks(self):
        self.assertEqual(len(self.plan.busy), 2)
        first = self.plan.busy[0]
        self.assertEqual(first.start, datetime(2026, 9, 14, 11, 0))
        self.assertEqual(first.end, datetime(2026, 9, 14, 12, 0))
        self.assertEqual(first.label, "standup with the team")

    def test_tasks(self):
        names = [task.name for task in self.plan.tasks]
        self.assertEqual(
            names, ["spec draft", "migration script", "code review", "slides"]
        )
        spec = self.plan.task("spec draft")
        self.assertEqual(spec.estimate, 240)
        self.assertEqual(spec.due, datetime(2026, 9, 15, 17, 0))
        self.assertEqual(spec.weight, 3.0)
        self.assertFalse(spec.required)
        self.assertTrue(self.plan.task("migration script").required)
        self.assertEqual(
            self.plan.task("code review").earliest, datetime(2026, 9, 14, 13, 30)
        )
        # A deadline written as a bare date means the end of that day.
        self.assertEqual(self.plan.task("slides").due, datetime(2026, 9, 18, 23, 59))

    def test_horizon(self):
        self.assertEqual(self.plan.horizon(), datetime(2026, 9, 18, 23, 59))

    def test_comments_and_blank_lines_are_ignored(self):
        text = "now: 2026-09-14 09:00  # start here\n\n\nhours:\n  mon: 09:00-10:00\n"
        plan = parse_plan(text)
        self.assertEqual(plan.now, datetime(2026, 9, 14, 9, 0))
        self.assertEqual(plan.tasks, ())

    def test_section_value_on_the_same_line(self):
        text = "now: 2026-09-14 09:00\nhours: mon: 09:00-10:00\n"
        plan = parse_plan(text)
        self.assertEqual(plan.hours[0], ((time(9, 0), time(10, 0)),))

    def test_task_names_may_contain_spaces_and_digits(self):
        text = (
            "now: 2026-09-14 09:00\nhours:\n  mon: 09:00-17:00\n"
            "tasks:\n  review PR 42 for auth  30m due 2026-09-14 17:00\n"
        )
        plan = parse_plan(text)
        self.assertEqual(plan.tasks[0].name, "review PR 42 for auth")


class PlanErrorTest(unittest.TestCase):
    def problems(self, text: str):
        with self.assertRaises(PlanError) as caught:
            parse_plan(textwrap.dedent(text))
        return caught.exception.problems

    def test_missing_now_and_hours(self):
        problems = self.problems("tasks:\n  a 1h due 2026-09-14 17:00\n")
        self.assertTrue(any("now" in problem for problem in problems))
        self.assertTrue(any("hours" in problem for problem in problems))

    def test_every_problem_is_reported_at_once(self):
        problems = self.problems(
            """
            now: 2026-09-14 09:00
            hours:
              funday: 09:00-10:00
            tasks:
              nodurationhere due 2026-09-15 12:00
              fine 1h due yesterday
            """
        )
        joined = " | ".join(problems)
        self.assertIn("funday", joined)
        self.assertIn("nodurationhere", joined)
        self.assertIn("yesterday", joined)
        # Every problem in the file is reported in one pass, not one per run.
        self.assertGreaterEqual(len(problems), 3, problems)

    def test_line_numbers_point_at_the_problem(self):
        problems = self.problems(
            "now: 2026-09-14 09:00\nhours:\n  mon: 25:00-26:00\n"
        )
        self.assertTrue(problems[0].startswith("line 3"), problems)

    def test_unknown_setting(self):
        problems = self.problems("now: 2026-09-14 09:00\ntimezone: UTC\nhours:\n  mon: 09:00-10:00\n")
        self.assertTrue(any("timezone" in problem for problem in problems))

    def test_indented_line_outside_a_section(self):
        problems = self.problems("  stray line\nnow: 2026-09-14 09:00\nhours:\n  mon: 09:00-10:00\n")
        self.assertTrue(any("outside any section" in problem for problem in problems))

    def test_overlapping_working_hours(self):
        problems = self.problems(
            "now: 2026-09-14 09:00\nhours:\n  mon: 09:00-12:00, 11:00-13:00\n"
        )
        self.assertTrue(any("overlap" in problem for problem in problems))

    def test_backwards_ranges(self):
        problems = self.problems("now: 2026-09-14 09:00\nhours:\n  mon: 17:00-09:00\n")
        self.assertTrue(any("ends before it starts" in problem for problem in problems))

    def test_duplicate_task_name(self):
        problems = self.problems(
            """
            now: 2026-09-14 09:00
            hours:
              mon: 09:00-17:00
            tasks:
              review 1h due 2026-09-14 17:00
              review 2h due 2026-09-15 17:00
            """
        )
        self.assertTrue(any("already used" in problem for problem in problems))

    def test_deadline_in_the_past(self):
        problems = self.problems(
            """
            now: 2026-09-14 09:00
            hours:
              mon: 09:00-17:00
            tasks:
              late thing 1h due 2026-09-13 17:00
            """
        )
        self.assertTrue(any("before 'now'" in problem for problem in problems))

    def test_earliest_after_deadline(self):
        problems = self.problems(
            """
            now: 2026-09-14 09:00
            hours:
              mon: 09:00-17:00
            tasks:
              thing 1h due 2026-09-14 12:00 earliest 2026-09-14 13:00
            """
        )
        self.assertTrue(any("after its deadline" in problem for problem in problems))

    def test_bad_weight(self):
        for value in ("0", "-1", "many"):
            problems = self.problems(
                f"now: 2026-09-14 09:00\nhours:\n  mon: 09:00-17:00\n"
                f"tasks:\n  thing 1h due 2026-09-14 17:00 weight {value}\n"
            )
            self.assertTrue(problems, value)

    def test_unexpected_keyword_in_task_line(self):
        problems = self.problems(
            "now: 2026-09-14 09:00\nhours:\n  mon: 09:00-17:00\n"
            "tasks:\n  thing 1h due 2026-09-14 17:00 urgent\n"
        )
        self.assertTrue(any("urgent" in problem for problem in problems))

    def test_busy_block_needs_a_range(self):
        problems = self.problems(
            "now: 2026-09-14 09:00\nhours:\n  mon: 09:00-17:00\nbusy:\n  2026-09-14\n"
        )
        self.assertTrue(problems)

    def test_empty_file(self):
        problems = self.problems("")
        self.assertEqual(len(problems), 2)


class LoadPlanTest(unittest.TestCase):
    def test_round_trip_from_disk(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.txt"
            path.write_text(GOOD, encoding="utf-8")
            plan = load_plan(str(path))
        self.assertEqual(len(plan.tasks), 4)

    def test_missing_file(self):
        with self.assertRaises(PlanError) as caught:
            load_plan("/nonexistent/plan.txt")
        self.assertIn("no such plan file", caught.exception.problems[0])

    def test_directory_instead_of_file(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(PlanError) as caught:
                load_plan(directory)
        self.assertIn("is a directory", caught.exception.problems[0])

    def test_not_utf8(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.txt"
            path.write_bytes(b"now: 2026-09-14 09:00\n\xff\xfe\n")
            with self.assertRaises(PlanError) as caught:
                load_plan(str(path))
        self.assertIn("not valid UTF-8", caught.exception.problems[0])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
