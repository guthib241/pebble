import json

import pytest
from conftest import fixture_path

from backfire import cli, config


def run(args, capsys):
    code = cli.main(args)
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def test_clean_project_exits_zero(capsys):
    code, out, _ = run([fixture_path("clean")], capsys)
    assert code == 0
    assert "No retry amplification findings." in out


def test_findings_exit_one(capsys):
    code, out, _ = run([fixture_path("unbounded")], capsys)
    assert code == 1
    assert "BF002" in out


def test_fail_on_none_always_exits_zero(capsys):
    code, _, _ = run([fixture_path("unbounded"), "--fail-on", "none"], capsys)
    assert code == 0


def test_fail_on_warning_catches_warnings(capsys):
    code, _, _ = run([fixture_path("layered"), "--fail-on", "warning"], capsys)
    assert code == 1
    code, _, _ = run([fixture_path("layered")], capsys)
    assert code == 0  # the layered finding is a warning, not an error


def test_max_attempts_flag(capsys):
    code, out, _ = run([fixture_path("layered"), "--max-attempts", "100"], capsys)
    assert code == 0
    assert "No retry amplification findings." in out


def test_json_output_shape(capsys):
    code, out, _ = run([fixture_path("layered"), "--json"], capsys)
    payload = json.loads(out)
    assert code == 0
    assert payload["findings"][0]["rule"] == "BF001"
    assert payload["findings"][0]["file"].endswith("client.py")
    assert payload["hot_paths"][0]["attempts"] == "30"
    assert payload["stats"]["functions"] == 5


def test_budget_flag(capsys):
    code, out, _ = run([fixture_path("layered"), "--budget", "handle_request=10s"], capsys)
    assert code == 1
    assert "BF005" in out


def test_bad_budget_is_a_usage_error(capsys):
    with pytest.raises(SystemExit) as error:
        cli.main([fixture_path("clean"), "--budget", "oops"])
    assert error.value.code == cli.EXIT_USAGE


def test_missing_path_is_a_usage_error(capsys):
    with pytest.raises(SystemExit) as error:
        cli.main(["/nonexistent/path/backfire"])
    assert error.value.code == cli.EXIT_USAGE


def test_unparsable_file_is_reported_and_skipped(tmp_path, capsys):
    (tmp_path / "broken.py").write_text("def f(:\n    pass\n")
    (tmp_path / "fine.py").write_text("def g():\n    return 1\n")
    code, out, err = run([str(tmp_path)], capsys)
    assert code == 0
    assert "skipped broken.py" in err
    assert "2 files" in out or "functions" in out


def test_no_evidence_flag(capsys):
    _, with_evidence, _ = run([fixture_path("layered"), "--fail-on", "none"], capsys)
    _, without, _ = run([fixture_path("layered"), "--fail-on", "none", "--no-evidence"], capsys)
    assert "    via " in with_evidence
    assert "    via " not in without


def test_config_file_is_picked_up(tmp_path, capsys):
    (tmp_path / "app.py").write_text(
        "import requests, time\n"
        "def poll(url):\n"
        "    for i in range(20):\n"
        "        try:\n"
        "            return requests.get(url, timeout=1)\n"
        "        except OSError:\n"
        "            time.sleep(1)\n"
    )
    (tmp_path / "backfire.toml").write_text("max_attempts = 50\n")
    code, out, _ = run([str(tmp_path)], capsys)
    assert code == 0
    assert "No retry amplification findings." in out
    code, out, _ = run([str(tmp_path), "--no-config"], capsys)
    assert "BF001" in out


def test_pyproject_config_with_budgets(tmp_path, capsys):
    (tmp_path / "app.py").write_text(
        "import requests\n"
        "from tenacity import retry, stop_after_attempt\n"
        "@retry(stop=stop_after_attempt(3))\n"
        "def fetch(url):\n"
        "    return requests.get(url, timeout=10)\n"
    )
    (tmp_path / "pyproject.toml").write_text(
        "[tool.backfire]\nmax_attempts = 100\n\n[tool.backfire.budgets]\nfetch = '5s'\n"
    )
    code, out, _ = run([str(tmp_path)], capsys)
    assert code == 1
    assert "BF005" in out


def test_parse_duration_units():
    assert config.parse_duration("500ms") == 0.5
    assert config.parse_duration("30s") == 30
    assert config.parse_duration("1.5m") == 90
    assert config.parse_duration("2h") == 7200
    assert config.parse_duration(3) == 3.0
    with pytest.raises(config.ConfigError):
        config.parse_duration("soon")


def test_version_flag(capsys):
    with pytest.raises(SystemExit) as error:
        cli.main(["--version"])
    assert error.value.code == 0
    assert "backfire" in capsys.readouterr().out


def test_ignore_comment_suppresses_a_finding(tmp_path, capsys):
    source = (
        "import requests, time\n"
        "def poll(url):\n"
        "    while True:  # backfire: ignore\n"
        "        try:\n"
        "            return requests.get(url, timeout=1)\n"
        "        except OSError:\n"
        "            time.sleep(1)\n"
    )
    (tmp_path / "app.py").write_text(source)
    code, out, _ = run([str(tmp_path)], capsys)
    assert "BF002" not in out
    assert "BF001" in out  # the amplification finding is on another line
    code, out, _ = run([str(tmp_path), "--fail-on", "none"], capsys)
    assert code == 0


def test_ignore_comment_can_name_rules(tmp_path, capsys):
    (tmp_path / "app.py").write_text(
        "import requests, time\n"
        "def poll(url):\n"
        "    while True:  # backfire: ignore[BF003]\n"
        "        try:\n"
        "            return requests.get(url, timeout=1)\n"
        "        except OSError:\n"
        "            time.sleep(1)\n"
    )
    _, out, _ = run([str(tmp_path), "--fail-on", "none"], capsys)
    assert "BF002" in out  # only BF003 was named, so BF002 still reports
