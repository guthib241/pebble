"""Tests for the command line interface, file discovery and error handling."""

from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from orbiter.analyze import analyze_paths, collect_python_files
from orbiter.cli import EXIT_CLEAN, EXIT_ERROR, EXIT_FINDINGS, main
from orbiter.config import ConfigError, load_config

FIXTURES = Path(__file__).parent / "fixtures" / "sample_project"
REPO_ROOT = Path(__file__).resolve().parents[1]


def run_cli(*argv: str):
    """Run the CLI in-process, returning (exit code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class CliTest(unittest.TestCase):
    def test_findings_exit_code_and_output(self):
        code, out, _ = run_cli(str(FIXTURES))
        self.assertEqual(code, EXIT_FINDINGS)
        self.assertIn("ORB001", out)
        self.assertIn("5 finding(s) in 2 file(s)", out)

    def test_clean_file_exits_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "clean.py"
            path.write_text("def add(left_ms, right_ms):\n    return left_ms + right_ms\n")
            code, out, _ = run_cli(str(path))
        self.assertEqual(code, EXIT_CLEAN)
        self.assertIn("0 finding(s)", out)

    def test_json_output_shape(self):
        code, out, _ = run_cli(str(FIXTURES), "--format", "json")
        self.assertEqual(code, EXIT_FINDINGS)
        payload = json.loads(out)
        self.assertEqual(payload["files_analysed"], 2)
        self.assertEqual(payload["errors"], [])
        self.assertEqual(len(payload["findings"]), 5)
        finding = payload["findings"][0]
        self.assertEqual(
            sorted(finding), ["code", "column", "line", "message", "path"]
        )
        self.assertTrue(finding["line"] > 0)

    def test_disable_reduces_findings(self):
        _, full, _ = run_cli(str(FIXTURES), "--format", "json")
        _, reduced, _ = run_cli(
            str(FIXTURES), "--format", "json", "--disable", "ORB001"
        )
        self.assertEqual(len(json.loads(full)["findings"]), 5)
        codes = {item["code"] for item in json.loads(reduced)["findings"]}
        self.assertNotIn("ORB001", codes)

    def test_unknown_disable_code_is_a_usage_error(self):
        with self.assertRaises(SystemExit) as caught:
            run_cli(str(FIXTURES), "--disable", "ORB999")
        self.assertEqual(caught.exception.code, 2)

    def test_no_paths_is_a_usage_error(self):
        with self.assertRaises(SystemExit) as caught:
            run_cli()
        self.assertEqual(caught.exception.code, 2)

    def test_list_units(self):
        code, out, _ = run_cli("--list-units")
        self.assertEqual(code, EXIT_CLEAN)
        self.assertIn("time (base unit: seconds)", out)
        self.assertIn("milliseconds: millis, millisecond, milliseconds, ms", out)
        self.assertIn("ORB001", out)

    def test_missing_path_is_reported_as_an_error(self):
        code, out, _ = run_cli("does_not_exist.py")
        self.assertEqual(code, EXIT_ERROR)
        self.assertIn("no such file or directory", out)

    def test_syntax_error_is_reported_without_crashing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.py"
            path.write_text("def f(:\n    pass\n")
            code, out, _ = run_cli(str(path))
        self.assertEqual(code, EXIT_ERROR)
        self.assertIn("syntax error", out)

    def test_non_utf8_file_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "latin.py"
            path.write_bytes(b"x = '\xff\xfe'\n")
            code, out, _ = run_cli(str(path))
        self.assertEqual(code, EXIT_ERROR)
        self.assertIn("not valid UTF-8", out)

    def test_empty_file_is_clean(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.py"
            path.write_text("")
            code, _, _ = run_cli(str(path))
        self.assertEqual(code, EXIT_CLEAN)

    def test_version_flag(self):
        with self.assertRaises(SystemExit) as caught:
            run_cli("--version")
        self.assertEqual(caught.exception.code, 0)


class ConfigFileTest(unittest.TestCase):
    def test_alias_and_extra_function(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "code.py").write_text(
                "import mylib\n\n"
                "def go(tmo):\n"
                "    mylib.pause(tmo)\n"
            )
            (root / "orbiter.toml").write_text(
                '[orbiter.aliases]\ntmo = "ms"\n\n'
                '[orbiter.functions."mylib.pause"]\n'
                'params = { 0 = "seconds" }\n'
            )
            code, out, _ = run_cli(
                str(root / "code.py"), "--config", str(root / "orbiter.toml")
            )
        self.assertEqual(code, EXIT_FINDINGS)
        self.assertIn("ORB001", out)
        self.assertIn("expects seconds", out)

    def test_disable_and_strict_from_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "code.py").write_text(
                "def copy(size_kb, other_kib):\n    return size_kb + other_kib\n"
            )
            (root / "orbiter.toml").write_text(
                "[orbiter]\nstrict_binary_prefixes = true\n"
            )
            code, out, _ = run_cli(
                str(root / "code.py"), "--config", str(root / "orbiter.toml")
            )
            self.assertEqual(code, EXIT_FINDINGS)
            self.assertIn("ORB002", out)

            (root / "off.toml").write_text(
                '[orbiter]\nstrict_binary_prefixes = true\ndisable = ["ORB002"]\n'
            )
            code, _, _ = run_cli(
                str(root / "code.py"), "--config", str(root / "off.toml")
            )
            self.assertEqual(code, EXIT_CLEAN)

    def test_config_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bad_unit = root / "bad_unit.toml"
            bad_unit.write_text('[orbiter.aliases]\ntmo = "parsecs"\n')
            with self.assertRaises(ConfigError):
                load_config(bad_unit)

            bad_code = root / "bad_code.toml"
            bad_code.write_text('[orbiter]\ndisable = ["NOPE1"]\n')
            with self.assertRaises(ConfigError):
                load_config(bad_code)

            bad_toml = root / "bad.toml"
            bad_toml.write_text("[orbiter\n")
            with self.assertRaises(ConfigError):
                load_config(bad_toml)

            with self.assertRaises(ConfigError):
                load_config(root / "missing.toml")

    def test_config_error_exits_with_error_code(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.toml"
            path.write_text('[orbiter.aliases]\ntmo = "parsecs"\n')
            code, _, err = run_cli(str(FIXTURES), "--config", str(path))
        self.assertEqual(code, EXIT_ERROR)
        self.assertIn("unknown unit", err)


class DiscoveryTest(unittest.TestCase):
    def test_directories_are_walked_and_caches_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pkg").mkdir()
            (root / "pkg" / "a.py").write_text("x = 1\n")
            (root / "pkg" / "__pycache__").mkdir()
            (root / "pkg" / "__pycache__" / "a.py").write_text("x = 1\n")
            (root / ".venv").mkdir()
            (root / ".venv" / "b.py").write_text("x = 1\n")
            (root / "notes.txt").write_text("not python\n")
            files, errors = collect_python_files([root])
        self.assertEqual([path.name for path in files], ["a.py"])
        self.assertEqual(errors, [])

    def test_duplicate_paths_are_analysed_once(self):
        path = FIXTURES / "scheduler.py"
        files, _ = collect_python_files([path, path, FIXTURES])
        self.assertEqual(len([item for item in files if item.name == "scheduler.py"]), 1)

    def test_explicit_file_in_a_skipped_directory_is_still_analysed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "build"
            root.mkdir()
            path = root / "gen.py"
            path.write_text("import time\n\ndef f(t_ms):\n    time.sleep(t_ms)\n")
            diagnostics, errors = analyze_paths([path], load_config())
        self.assertEqual(errors, [])
        self.assertEqual([item.code for item in diagnostics], ["ORB001"])


class InstallationTest(unittest.TestCase):
    """The documented usage path must work from a clean checkout."""

    def test_module_entry_point(self):
        result = subprocess.run(
            [sys.executable, "-m", "orbiter", str(FIXTURES)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, EXIT_FINDINGS, result.stderr)
        self.assertIn("ORB001", result.stdout)

    def test_self_analysis_is_clean(self):
        """orbiter's own source must be free of unit findings."""
        result = subprocess.run(
            [sys.executable, "-m", "orbiter", "orbiter"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, EXIT_CLEAN, result.stdout + result.stderr)

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
            script = environment / "bin" / "orbiter"
            if not script.exists():  # pragma: no cover - platform dependent
                script = environment / "Scripts" / "orbiter.exe"
            self.assertTrue(script.exists(), "console script was not installed")
            result = subprocess.run(
                [str(script), str(FIXTURES)], capture_output=True, text=True
            )
            self.assertEqual(result.returncode, EXIT_FINDINGS, result.stderr)
            self.assertIn("ORB004", result.stdout)
            self.assertIn("5 finding(s) in 2 file(s)", result.stdout)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
