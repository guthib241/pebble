import ast
import math

import pytest

from backfire import detect
from backfire.parse import loop_retry_policy


def decorator(source: str):
    tree = ast.parse(source)
    return tree.body[0].decorator_list[0]


def call(source: str) -> ast.Call:
    return ast.parse(source).body[0].value


def test_tenacity_attempt_stop():
    policy = detect.decorator_policy(
        decorator("@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))\ndef f(): pass")
    )
    assert policy.source == "tenacity"
    assert policy.attempts == 5
    assert policy.backoff is True
    assert policy.wait_total == pytest.approx(8.0)  # four gaps of two seconds


def test_tenacity_without_stop_is_unbounded():
    policy = detect.decorator_policy(decorator("@retry(wait=wait_fixed(1))\ndef f(): pass"))
    assert math.isinf(policy.attempts)
    assert policy.unbounded is True


def test_bare_tenacity_decorator():
    policy = detect.decorator_policy(decorator("@retry\ndef f(): pass"))
    assert math.isinf(policy.attempts)


def test_tenacity_stop_after_delay_is_time_capped():
    policy = detect.decorator_policy(decorator("@retry(stop=stop_after_delay(30))\ndef f(): pass"))
    assert math.isinf(policy.attempts)
    assert policy.max_seconds == 30
    assert policy.unbounded is False


def test_tenacity_combined_stop_conditions():
    policy = detect.decorator_policy(
        decorator("@retry(stop=(stop_after_attempt(4) | stop_after_delay(9)))\ndef f(): pass")
    )
    assert policy.attempts == 4
    assert policy.max_seconds == 9


def test_tenacity_exponential_wait_is_bounded_by_max():
    policy = detect.decorator_policy(
        decorator(
            "@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, max=4))\ndef f(): pass"
        )
    )
    # gaps are 1, 2, 4 then capped at 4
    assert policy.wait_total == pytest.approx(11.0)


def test_tenacity_non_literal_attempts_is_marked_unknown():
    policy = detect.decorator_policy(
        decorator("@retry(stop=stop_after_attempt(CONFIG.tries))\ndef f(): pass")
    )
    assert policy.attempts_known is False


def test_backoff_decorator():
    policy = detect.decorator_policy(
        decorator("@backoff.on_exception(backoff.expo, OSError, max_tries=4, max_time=30)\ndef f(): pass")
    )
    assert policy.source == "backoff"
    assert policy.attempts == 4
    assert policy.max_seconds == 30


def test_backoff_without_max_tries_is_unbounded():
    policy = detect.decorator_policy(decorator("@backoff.on_exception(backoff.expo, OSError)\ndef f(): pass"))
    assert math.isinf(policy.attempts)


def test_stamina_defaults_are_library_documented():
    policy = detect.decorator_policy(decorator("@stamina.retry(on=OSError)\ndef f(): pass"))
    assert policy.attempts == detect.STAMINA_DEFAULT_ATTEMPTS
    assert policy.max_seconds == detect.STAMINA_DEFAULT_TIMEOUT


def test_celery_autoretry_uses_max_retries_plus_one():
    policy = detect.decorator_policy(
        decorator("@app.task(autoretry_for=(OSError,), max_retries=5)\ndef f(): pass")
    )
    assert policy.attempts == 6


def test_celery_task_without_autoretry_is_not_a_retry():
    assert detect.decorator_policy(decorator("@app.task(queue='mail')\ndef f(): pass")) is None


def test_plain_decorator_is_ignored():
    assert detect.decorator_policy(decorator("@functools.cache\ndef f(): pass")) is None


def test_urllib3_retry_counts_attempts_not_retries():
    policy = detect.transport_policy(call("Retry(total=4, backoff_factor=0.5)"))
    assert policy.attempts == 5
    assert policy.backoff is True
    # urllib3 sleeps factor * 2**(n-1) before retry n, and not at all before the first
    assert policy.wait_total == pytest.approx(7.0)  # 0.5 * (2 + 4 + 8)


def test_urllib3_retry_default_total():
    policy = detect.transport_policy(call("Retry()"))
    assert policy.attempts == detect.URLLIB3_DEFAULT_TOTAL + 1
    assert policy.backoff is False


def test_http_adapter_integer_retries():
    policy = detect.transport_policy(call("HTTPAdapter(max_retries=2)"))
    assert policy.attempts == 3


def test_httpx_transport_retries():
    policy = detect.transport_policy(call("httpx.HTTPTransport(retries=3)"))
    assert policy.attempts == 4


def test_timeout_forms():
    assert detect.timeout_seconds(call("requests.get(url, timeout=3)")) == (3.0, True)
    assert detect.timeout_seconds(call("requests.get(url, timeout=(1, 4))")) == (5.0, True)
    assert detect.timeout_seconds(call("requests.get(url)")) == (math.inf, True)
    seconds, known = detect.timeout_seconds(call("requests.get(url, timeout=CONFIG.t)"))
    assert math.isinf(seconds) and known is False


def test_httpx_timeout_object():
    seconds, known = detect.timeout_seconds(call("client.get(url, timeout=httpx.Timeout(2, connect=4))"))
    assert (seconds, known) == (4.0, True)


def test_http_call_recognition():
    assert detect.is_http_module_call("requests.get")
    assert detect.is_http_module_call("httpx.post")
    assert not detect.is_http_module_call("json.get")
    assert detect.is_urlopen("urllib.request.urlopen")
    assert detect.is_subprocess("subprocess.run")
    assert detect.is_sleep("time.sleep")


def test_wait_for_deadline():
    assert detect.wait_for_deadline(call("asyncio.wait_for(task, timeout=3)")) == 3.0
    assert detect.wait_for_deadline(call("asyncio.wait_for(task, 4)")) == 4.0
    assert detect.wait_for_deadline(call("other.wait_for(task, 4)")) is None


def loop(source: str):
    return ast.parse(source).body[0]


def test_for_range_retry_loop():
    policy = loop_retry_policy(
        loop(
            "for attempt in range(3):\n"
            "    try:\n"
            "        return work()\n"
            "    except OSError:\n"
            "        time.sleep(1)\n"
        )
    )
    assert policy.attempts == 3
    assert policy.backoff is True


def test_while_true_retry_loop_is_unbounded():
    policy = loop_retry_policy(
        loop("while True:\n    try:\n        return work()\n    except OSError:\n        continue\n")
    )
    assert math.isinf(policy.attempts)
    assert policy.backoff is False


def test_plain_loop_is_not_a_retry():
    assert loop_retry_policy(loop("for item in items:\n    handle(item)\n")) is None
    assert (
        loop_retry_policy(loop("for i in range(3):\n    total += i\n")) is None
    )


def test_loop_with_non_literal_range_is_estimated():
    policy = loop_retry_policy(
        loop(
            "for attempt in range(settings.tries):\n"
            "    try:\n"
            "        return work()\n"
            "    except OSError:\n"
            "        continue\n"
        )
    )
    assert policy.attempts_known is False


def test_loop_that_only_swallows_errors_is_not_a_retry():
    # a fan-out loop, not a retry: nothing exits early and nothing waits
    assert (
        loop_retry_policy(
            loop(
                "for index in range(5):\n"
                "    try:\n"
                "        results.append(fetch(index))\n"
                "    except OSError:\n"
                "        pass\n"
            )
        )
        is None
    )


def test_streaming_loop_that_returns_only_in_handler_is_not_a_retry():
    assert (
        loop_retry_policy(
            loop(
                "while True:\n"
                "    try:\n"
                "        yield conn.recv()\n"
                "    except ConnectionClosedOK:\n"
                "        return\n"
            )
        )
        is None
    )


def test_backoff_outside_the_handler_still_counts():
    policy = loop_retry_policy(
        loop(
            "for attempt in range(3):\n"
            "    delay = 2 ** attempt\n"
            "    try:\n"
            "        return work()\n"
            "    except OSError:\n"
            "        pass\n"
            "    time.sleep(delay)\n"
        )
    )
    assert policy.attempts == 3
    assert policy.backoff is True


def test_anyio_sleep_is_a_sleep():
    assert detect.is_sleep("anyio.sleep")
    assert detect.is_sleep("trio.sleep")
