"""Tests for the command line interface, output formats and error handling."""

from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from cutline.analysis import analyse
from cutline.cli import EXIT_DOES_NOT_FIT, EXIT_ERROR, EXIT_FITS, main, parse_accept
from cutline.plan import PlanError, load_plan, parse_plan
from cutline.report import render_json, render_text

FIXTURES = Path(__file__).parent / "fixtures"
WEEK = FIXTURES / "week.txt"
FITS = FIXTURES / "fits.txt"
IMPOSSIBLE = FIXTURES / "impossible.txt"
REPO_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*argv: str, stdin: str = ""):
    """Run the CLI in-process, returning (exit code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    saved = sys.stdin
    sys.stdin = io.StringIO(stdin)
    try:
        with redirect_stdout(out), redirect_stderr(err):
            code = main(list(argv))
    finally:
        sys.stdin = saved
    return code, out.getvalue(), err.getvalue()


class VerdictTest(unittest.TestCase):
    def test_plan_that_fits(self):
        code, out, _ = run_cli(str(FITS))
        self.assertEqual(code, EXIT_FITS)
        self.assertIn("VERDICT: fits", out)
        self.assertIn("tightest deadline", out)

    def test_plan_that_does_not_fit(self):
        code, out, _ = run_cli(str(WEEK))
        self.assertEqual(code, EXIT_DOES_NOT_FIT)
        self.assertIn("VERDICT: does not fit", out)
        self.assertIn("over-subscribed window", out)
        self.assertIn("cheapest cut", out)
        self.assertIn("proven minimal", out)
        self.assertIn("keep it by moving its deadline to", out)

    def test_impossible_plan_says_so(self):
        code, out, _ = run_cli(str(IMPOSSIBLE))
        self.assertEqual(code, EXIT_DOES_NOT_FIT)
        self.assertIn("no cut can fix this", out)
        self.assertIn("release rehearsal", out)

    def test_empty_task_list_fits(self):
        code, out, _ = run_cli(
            "-", stdin="now: 2026-09-14 09:00\nhours:\n  mon: 09:00-17:00\n"
        )
        self.assertEqual(code, EXIT_FITS)
        self.assertIn("VERDICT: fits", out)
        self.assertIn("standard input", out)


class OutputTest(unittest.TestCase):
    def test_schedule_section(self):
        _, out, _ = run_cli(str(FITS), "--schedule")
        self.assertIn("schedule (earliest deadline first)", out)
        self.assertIn("spec draft", out)

    def test_slack_section(self):
        _, out, _ = run_cli(str(FITS), "--slack")
        self.assertIn("spare capacity for new work, by deadline", out)

    def test_json_shape(self):
        code, out, _ = run_cli(str(WEEK), "--json")
        self.assertEqual(code, EXIT_DOES_NOT_FIT)
        payload = json.loads(out)
        self.assertFalse(payload["feasible"])
        self.assertTrue(payload["methods_agree"])
        self.assertEqual(payload["task_count"], 4)
        self.assertTrue(payload["windows"])
        self.assertTrue(payload["cut"]["dropped"])
        self.assertTrue(payload["cut"]["proven_minimal"])
        window = payload["windows"][0]
        self.assertEqual(
            window["deficit_minutes"], window["work_minutes"] - window["capacity_minutes"]
        )
        self.assertEqual(
            sorted(payload),
            [
                "capacity_minutes",
                "committed_minutes",
                "cut",
                "feasible",
                "horizon",
                "methods_agree",
                "now",
                "schedule",
                "slack",
                "slack_after_cut",
                "source",
                "task_count",
                "tasks",
                "unplaced",
                "windows",
            ],
        )

    def test_json_is_valid_for_a_feasible_plan(self):
        code, out, _ = run_cli(str(FITS), "--json")
        self.assertEqual(code, EXIT_FITS)
        payload = json.loads(out)
        self.assertTrue(payload["feasible"])
        self.assertEqual(payload["windows"], [])
        self.assertEqual(payload["cut"]["dropped"], [])
        self.assertEqual(payload["unplaced"], {})

    def test_example_plan_is_parseable_and_printed(self):
        code, out, _ = run_cli("--example")
        self.assertEqual(code, EXIT_FITS)
        plan = parse_plan(out)
        self.assertEqual(len(plan.tasks), 4)

    def test_text_and_json_agree_on_the_verdict(self):
        for fixture in (WEEK, FITS, IMPOSSIBLE):
            plan = load_plan(str(fixture))
            analysis = analyse(plan, source=str(fixture))
            text = render_text(analysis)
            payload = json.loads(render_json(analysis))
            self.assertEqual(
                payload["feasible"], "VERDICT: fits" in text, f"{fixture} disagrees"
            )


class AcceptTest(unittest.TestCase):
    def test_accepting_a_small_task_still_fits(self):
        code, out, _ = run_cli(str(FITS), "--accept", "quick call:30m@2026-09-18 17:00")
        self.assertEqual(code, EXIT_FITS)
        self.assertIn("quick call", out)
        self.assertIn("VERDICT: fits", out)

    def test_accepting_too_much_work_does_not_fit(self):
        code, out, _ = run_cli(str(FITS), "--accept", "rewrite:30h@2026-09-16 17:00")
        self.assertEqual(code, EXIT_DOES_NOT_FIT)
        self.assertIn("rewrite", out)

    def test_bare_date_deadline(self):
        code, _, _ = run_cli(str(FITS), "--accept", "quick call:30m@2026-09-18")
        self.assertEqual(code, EXIT_FITS)

    def test_bad_accept_specs_are_usage_errors(self):
        for spec in (
            "no separators",
            ":30m@2026-09-18",
            "name:notaduration@2026-09-18",
            "name:30m@not-a-date",
            "name:30m@2026-09-01",
        ):
            code, _, err = run_cli(str(FITS), "--accept", spec)
            self.assertEqual(code, EXIT_ERROR, spec)
            self.assertTrue(err.strip(), spec)

    def test_accept_name_may_not_collide(self):
        code, _, err = run_cli(str(FITS), "--accept", "slides:30m@2026-09-18")
        self.assertEqual(code, EXIT_ERROR)
        self.assertIn("already used", err)

    def test_parse_accept_returns_a_task(self):
        plan = load_plan(str(FITS))
        task = parse_accept("call:1h30m@2026-09-18 12:00", plan)
        self.assertEqual(task.name, "call")
        self.assertEqual(task.estimate, 90)

    def test_parse_accept_rejects_nonsense(self):
        plan = load_plan(str(FITS))
        with self.assertRaises(PlanError):
            parse_accept("nonsense", plan)


class NowOverrideTest(unittest.TestCase):
    def test_later_now_reduces_capacity(self):
        _, early, _ = run_cli(str(FITS), "--json")
        _, late, _ = run_cli(str(FITS), "--now", "2026-09-14 16:00", "--json")
        self.assertGreater(
            json.loads(early)["capacity_minutes"], json.loads(late)["capacity_minutes"]
        )

    def test_now_past_a_deadline_is_an_error(self):
        code, _, err = run_cli(str(FITS), "--now", "2026-09-19 09:00")
        self.assertEqual(code, EXIT_ERROR)
        self.assertIn("deadline", err)

    def test_unparseable_now(self):
        code, _, err = run_cli(str(FITS), "--now", "tomorrow")
        self.assertEqual(code, EXIT_ERROR)
        self.assertTrue(err.strip())


class ErrorHandlingTest(unittest.TestCase):
    def test_missing_plan_file(self):
        code, _, err = run_cli("/nonexistent/plan.txt")
        self.assertEqual(code, EXIT_ERROR)
        self.assertIn("no such plan file", err)

    def test_every_parse_problem_is_printed(self):
        code, _, err = run_cli("-", stdin="tasks:\n  broken line\n")
        self.assertEqual(code, EXIT_ERROR)
        self.assertGreaterEqual(len(err.strip().splitlines()), 2)

    def test_directory_as_plan(self):
        with tempfile.TemporaryDirectory() as directory:
            code, _, err = run_cli(directory)
        self.assertEqual(code, EXIT_ERROR)
        self.assertIn("directory", err)

    def test_no_arguments_is_a_usage_error(self):
        with self.assertRaises(SystemExit) as caught:
            run_cli()
        self.assertEqual(caught.exception.code, 2)

    def test_bad_flag_values(self):
        for flag, value in (("--budget", "0"), ("--defer-limit-days", "0")):
            with self.assertRaises(SystemExit) as caught:
                run_cli(str(FITS), flag, value)
            self.assertEqual(caught.exception.code, 2)

    def test_version(self):
        with self.assertRaises(SystemExit) as caught:
            run_cli("--version")
        self.assertEqual(caught.exception.code, 0)


class BudgetTest(unittest.TestCase):
    def test_small_budget_is_labelled_not_proven(self):
        code, out, _ = run_cli(str(WEEK), "--budget", "1")
        self.assertEqual(code, EXIT_DOES_NOT_FIT)
        self.assertIn("NOT proven minimal", out)

    def test_json_records_the_budget_outcome(self):
        _, out, _ = run_cli(str(WEEK), "--budget", "1", "--json")
        cut = json.loads(out)["cut"]
        self.assertFalse(cut["proven_minimal"])
        self.assertTrue(cut["budget_exhausted"])


class DeterminismTest(unittest.TestCase):
    def test_repeated_runs_produce_identical_output(self):
        first = run_cli(str(WEEK), "--json", "--schedule")
        second = run_cli(str(WEEK), "--json", "--schedule")
        self.assertEqual(first, second)


class InstallationTest(unittest.TestCase):
    """The documented usage path must work from a clean checkout."""

    def test_module_entry_point(self):
        result = subprocess.run(
            [sys.executable, "-m", "cutline", str(WEEK)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, EXIT_DOES_NOT_FIT, result.stderr)
        self.assertIn("cheapest cut", result.stdout)

    def test_package_installs_and_provides_a_console_script(self):
        """``pip install .`` into a fresh virtualenv yields a working command."""
        with tempfile.TemporaryDirectory() as directory:
            environment = Path(directory) / "venv"
            created = subprocess.run(
                [sys.executable, "-m", "venv", str(environment)],
                capture_output=True,
                text=True,
            )
            if created.returncode != 0:  # pragma: no cover - environment dependent
                self.skipTest(f"cannot create a virtualenv: {created.stderr[-200:]}")
            pip = environment / "bin" / "pip"
            if not pip.exists():  # pragma: no cover - platform dependent
                pip = environment / "Scripts" / "pip.exe"
            installed = subprocess.run(
                [str(pip), "install", "--no-build-isolation", "--no-deps", str(REPO_ROOT)],
                capture_output=True,
                text=True,
            )
            if installed.returncode != 0:  # pragma: no cover - environment dependent
                self.skipTest(f"pip install failed: {installed.stderr[-300:]}")
            script = environment / "bin" / "cutline"
            if not script.exists():  # pragma: no cover - platform dependent
                script = environment / "Scripts" / "cutline.exe"
            self.assertTrue(script.exists(), "console script was not installed")
            result = subprocess.run(
                [str(script), str(WEEK)], capture_output=True, text=True
            )
            self.assertEqual(result.returncode, EXIT_DOES_NOT_FIT, result.stderr)
            self.assertIn("VERDICT: does not fit", result.stdout)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
