import math

import pytest
from conftest import analyze_fixture, graph_of

from backfire.analyze import Options, analyze


def rules(report):
    return sorted({finding.rule for finding in report.findings})


def test_layered_amplification_is_the_product_of_three_layers(layered):
    record = layered.amplifications[0]
    # tenacity(3) x hand-rolled loop(2) x urllib3 Retry(total=4 -> 5 attempts)
    assert record.attempts == 30
    assert record.known is True
    assert record.path == [
        "api:handle_request",
        "service:UserService.fetch",
        "client:ApiClient.get_user",
    ]
    assert [finding.rule for finding in layered.findings] == ["BF001"]


def test_layered_evidence_names_every_layer(layered):
    evidence = " ".join(layered.findings[0].evidence)
    assert "tenacity" in evidence
    assert "loop" in evidence
    assert "urllib3" in evidence


def test_layered_worst_case_duration():
    report = analyze_fixture("layered", Options(budgets={"handle_request": 30.0}))
    budget = [finding for finding in report.findings if finding.rule == "BF005"][0]
    # 5s timeout x 5 transport attempts + 7s urllib3 backoff = 32s per client call,
    # x2 loop attempts + 2s of sleeps = 66s, x3 tenacity attempts + 1s of waits = 199s
    assert budget.data["worst_case"] == pytest.approx(199.0)


def test_clean_project_has_no_findings():
    report = analyze_fixture("clean")
    assert report.findings == []
    assert report.amplifications[0].attempts == 3


def test_unbounded_loop_findings():
    report = analyze_fixture("unbounded")
    assert rules(report) == ["BF001", "BF002", "BF004"]
    assert math.isinf(report.amplifications[0].attempts)


def test_deadline_inversion_detected():
    report = analyze_fixture("deadline")
    finding = [item for item in report.findings if item.rule == "BF005"][0]
    assert finding.data["budget"] == 5.0
    assert finding.data["worst_case"] == pytest.approx(26.0)  # 4 attempts x 5s + 6s of waits


def test_threshold_controls_reporting(layered):
    quiet = analyze_fixture("layered", Options(max_attempts=30))
    assert [finding.rule for finding in quiet.findings] == []
    loud = analyze_fixture("layered", Options(max_attempts=5))
    assert [finding.rule for finding in loud.findings] == ["BF001"]


def test_severity_escalates_far_above_threshold():
    report = analyze_fixture("layered", Options(max_attempts=5))
    assert report.findings[0].severity == "error"  # 30 attempts is more than 3x the threshold
    report = analyze_fixture("layered", Options(max_attempts=20))
    assert report.findings[0].severity == "warning"


def test_retry_without_backoff_is_reported():
    report = analyze(
        graph_of(
            {
                "a": (
                    "from tenacity import retry, stop_after_attempt\n"
                    "@retry(stop=stop_after_attempt(5))\n"
                    "def f():\n"
                    "    return 1\n"
                )
            }
        )
    )
    assert rules(report) == ["BF003"]


def test_estimated_attempts_are_flagged():
    report = analyze(
        graph_of(
            {
                "a": (
                    "import requests, time\n"
                    "def f(url, settings):\n"
                    "    for i in range(settings.tries):\n"
                    "        try:\n"
                    "            return requests.get(url, timeout=1)\n"
                    "        except OSError:\n"
                    "            time.sleep(1)\n"
                )
            }
        ),
        Options(max_attempts=2),
    )
    finding = [item for item in report.findings if item.rule == "BF001"][0]
    assert finding.data["known"] is False
    assert "estimated" in finding.message


def test_recursive_retry_is_not_an_infinite_loop():
    report = analyze(
        graph_of(
            {
                "a": (
                    "from tenacity import retry, stop_after_attempt\n"
                    "@retry(stop=stop_after_attempt(3))\n"
                    "def f(n):\n"
                    "    return g(n)\n"
                    "def g(n):\n"
                    "    return f(n - 1)\n"
                )
            }
        )
    )
    assert isinstance(report.stats["functions"], int)


def test_max_depth_limits_path_length():
    sources = {
        "m": "".join(
            f"def f{index}():\n    return f{index + 1}()\n" for index in range(6)
        )
        + "import requests\ndef f6():\n    return requests.get('x', timeout=1)\n"
    }
    deep = analyze(graph_of(sources), Options(max_depth=10))
    shallow = analyze(graph_of(sources), Options(max_depth=2))
    assert deep.amplifications and not shallow.amplifications


def test_stats_are_reported(layered):
    assert layered.stats["functions"] == 5
    assert layered.stats["retry_sites"] == 3
    assert layered.stats["edges"] == 4


def test_module_constant_attempt_counts_are_resolved():
    report = analyze(
        graph_of(
            {
                "a": (
                    "import requests\n"
                    "from tenacity import retry, stop_after_attempt, wait_fixed\n"
                    "MAX_TRIES = 12\n"
                    "@retry(stop=stop_after_attempt(MAX_TRIES), wait=wait_fixed(1))\n"
                    "def f(url):\n"
                    "    return requests.get(url, timeout=1)\n"
                )
            }
        )
    )
    finding = [item for item in report.findings if item.rule == "BF001"][0]
    assert finding.data["attempts"] == 12
    assert finding.data["known"] is True


def test_unreadable_stop_is_estimated_not_called_unbounded():
    report = analyze(
        graph_of(
            {
                "a": (
                    "from tenacity import retry, wait_fixed\n"
                    "@retry(stop=settings.stop_policy, wait=wait_fixed(1))\n"
                    "def f():\n"
                    "    return 1\n"
                )
            }
        )
    )
    assert [item.rule for item in report.findings] == []  # no BF002: the cap is unreadable, not absent


def test_caught_timeout_is_not_a_budget_finding():
    sources = {
        "a": (
            "import asyncio\n"
            "from tenacity import retry, stop_after_attempt, wait_fixed\n"
            "import httpx\n"
            "@retry(stop=stop_after_attempt(4), wait=wait_fixed(2))\n"
            "async def work():\n"
            "    return httpx.get('https://x.invalid', timeout=5)\n"
            "async def poll():\n"
            "    while True:\n"
            "        try:\n"
            "            return await asyncio.wait_for(work(), timeout=1)\n"
            "        except asyncio.TimeoutError:\n"
            "            continue\n"
        )
    }
    report = analyze(graph_of(sources))
    assert [item.rule for item in report.findings if item.rule == "BF005"] == []
