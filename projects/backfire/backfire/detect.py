"""Recognition of retry policies, timeouts and blocking calls in an AST."""

from __future__ import annotations

import ast
import contextlib
import math

from .model import UNBOUNDED, RetryPolicy

# Attempt count used when a retry declares a count this analyzer cannot read
# (a computed expression, a value from settings). Findings built on it are
# marked as estimates.
ASSUMED_ATTEMPTS = 3.0

_CONSTANTS: dict[str, object] = {}


@contextlib.contextmanager
def constant_scope(mapping: dict):
    """Resolve module-level constants (``MAX_TRIES = 3``) while parsing a module."""
    global _CONSTANTS
    previous = _CONSTANTS
    _CONSTANTS = mapping
    try:
        yield
    finally:
        _CONSTANTS = previous

HTTP_METHODS = {
    "get",
    "post",
    "put",
    "patch",
    "delete",
    "head",
    "options",
    "request",
    "send",
    "stream",
}

# Library defaults that are documented behaviour, not guesses.
STAMINA_DEFAULT_ATTEMPTS = 10.0
STAMINA_DEFAULT_TIMEOUT = 45.0
CELERY_DEFAULT_MAX_RETRIES = 3.0
URLLIB3_DEFAULT_TOTAL = 10.0
URLLIB3_DEFAULT_BACKOFF_MAX = 120.0


def dotted_name(node: ast.AST) -> str | None:
    """Render a Name/Attribute chain as dotted text, or return None."""
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    elif isinstance(node, ast.Call):
        inner = dotted_name(node.func)
        if inner is None:
            return None
        parts.append(inner + "()")
    else:
        return None
    return ".".join(reversed(parts))


def literal(node: ast.AST | None):
    if node is None:
        return None
    if isinstance(node, ast.Name) and node.id in _CONSTANTS:
        return _CONSTANTS[node.id]
    try:
        return ast.literal_eval(node)
    except (ValueError, SyntaxError, TypeError):
        return None


def number(node: ast.AST | None) -> float | None:
    value = literal(node)
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def kwarg(call: ast.Call, name: str) -> ast.AST | None:
    for keyword in call.keywords:
        if keyword.arg == name:
            return keyword.value
    return None


def _call_of(node: ast.AST) -> ast.Call | None:
    return node if isinstance(node, ast.Call) else None


def _last(name: str | None) -> str:
    return (name or "").rsplit(".", 1)[-1]


# --------------------------------------------------------------------------
# tenacity
# --------------------------------------------------------------------------


def _tenacity_stop(node: ast.AST) -> tuple[float, float | None, bool]:
    """Return (attempts, max_seconds, known) for a tenacity stop condition."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.BitOr, ast.BitAnd)):
        left = _tenacity_stop(node.left)
        right = _tenacity_stop(node.right)
        attempts = min(left[0], right[0])
        seconds = [s for s in (left[1], right[1]) if s is not None]
        return attempts, (min(seconds) if seconds else None), left[2] and right[2]
    call = _call_of(node)
    if call is None:
        name = _last(dotted_name(node))
        if name == "stop_never":
            return UNBOUNDED, None, True
        return ASSUMED_ATTEMPTS, None, False  # a stop condition we cannot read
    name = _last(dotted_name(call.func))
    if name == "stop_after_attempt":
        value = number(call.args[0]) if call.args else number(kwarg(call, "max_attempt_number"))
        if value is None:
            return ASSUMED_ATTEMPTS, None, False
        return value, None, True
    if name == "stop_after_delay":
        value = number(call.args[0]) if call.args else number(kwarg(call, "max_delay"))
        return UNBOUNDED, value, value is not None
    if name == "stop_never":
        return UNBOUNDED, None, True
    return ASSUMED_ATTEMPTS, None, False  # a stop condition we cannot read


def _tenacity_wait(node: ast.AST, attempts: float) -> tuple[bool, float, bool]:
    """Return (has_backoff, worst-case total wait seconds, known)."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.BitOr, ast.BitAnd)):
        left = _tenacity_wait(node.left, attempts)
        right = _tenacity_wait(node.right, attempts)
        return (
            left[0] or right[0],
            left[1] + right[1],
            left[2] and right[2],
        )
    call = _call_of(node)
    if call is None:
        return True, 0.0, False
    name = _last(dotted_name(call.func))
    gaps = (attempts - 1) if math.isfinite(attempts) else math.inf
    if name == "wait_none":
        return False, 0.0, True
    if name == "wait_fixed":
        seconds = number(call.args[0]) if call.args else number(kwarg(call, "wait"))
        if seconds is None:
            return True, 0.0, False
        return True, seconds * gaps, True
    if name == "wait_random":
        high = number(kwarg(call, "max"))
        if high is None and len(call.args) > 1:
            high = number(call.args[1])
        if high is None:
            return True, 0.0, False
        return True, high * gaps, True
    if name in {"wait_exponential", "wait_random_exponential", "wait_exponential_jitter"}:
        multiplier = number(kwarg(call, "multiplier"))
        if multiplier is None and call.args:
            multiplier = number(call.args[0])
        if multiplier is None:
            multiplier = 1.0
        base = number(kwarg(call, "exp_base")) or 2.0
        cap = number(kwarg(call, "max"))
        if cap is None:
            cap = 3600.0  # tenacity's documented default ceiling
        if not math.isfinite(gaps):
            return True, math.inf, True
        total = 0.0
        for index in range(int(gaps)):
            total += min(multiplier * (base**index), cap)
        return True, total, True
    if name == "wait_incrementing":
        start = number(kwarg(call, "start")) or 0.0
        increment = number(kwarg(call, "increment")) or 0.0
        if not math.isfinite(gaps):
            return True, math.inf, True
        total = sum(start + increment * index for index in range(int(gaps)))
        return True, total, True
    return True, 0.0, False


def tenacity_policy(decorator: ast.AST) -> RetryPolicy | None:
    call = _call_of(decorator)
    name = dotted_name(decorator if call is None else call.func) or ""
    if _last(name) not in {"retry", "Retrying", "AsyncRetrying"}:
        return None
    head = name.rsplit(".", 1)[0] if "." in name else ""
    if head not in {"", "tenacity"}:
        return None
    if call is None:
        return RetryPolicy(
            source="tenacity",
            attempts=UNBOUNDED,
            detail="@retry with no stop condition retries forever",
        )
    stop_node = kwarg(call, "stop")
    if stop_node is None:
        attempts, max_seconds, attempts_known = UNBOUNDED, None, True
        detail = "no stop= given, so tenacity retries forever"
    else:
        attempts, max_seconds, attempts_known = _tenacity_stop(stop_node)
        detail = ast.unparse(stop_node)
    wait_node = kwarg(call, "wait")
    if wait_node is None:
        backoff, wait_total, wait_known = False, 0.0, True
    else:
        backoff, wait_total, wait_known = _tenacity_wait(wait_node, attempts)
    return RetryPolicy(
        source="tenacity",
        attempts=attempts,
        attempts_known=attempts_known,
        backoff=backoff,
        wait_total=wait_total,
        wait_known=wait_known,
        max_seconds=max_seconds,
        detail=detail,
    )


# --------------------------------------------------------------------------
# backoff / stamina / celery
# --------------------------------------------------------------------------


def backoff_policy(decorator: ast.AST) -> RetryPolicy | None:
    call = _call_of(decorator)
    if call is None:
        return None
    name = dotted_name(call.func) or ""
    if _last(name) not in {"on_exception", "on_predicate"}:
        return None
    max_tries_node = kwarg(call, "max_tries")
    max_tries = number(max_tries_node)
    attempts_known = max_tries_node is None or max_tries is not None
    if max_tries is None and max_tries_node is not None:
        max_tries = ASSUMED_ATTEMPTS
    max_time = number(kwarg(call, "max_time"))
    wait_gen = _last(dotted_name(call.args[0])) if call.args else ""
    has_backoff = wait_gen != "constant" or number(kwarg(call, "interval")) != 0
    attempts = max_tries if max_tries is not None else UNBOUNDED
    detail = f"backoff.{wait_gen}" if wait_gen else "backoff"
    if max_tries is None:
        detail += ", no max_tries (unbounded attempts)"
    return RetryPolicy(
        source="backoff",
        attempts=attempts,
        attempts_known=attempts_known,
        backoff=has_backoff,
        wait_total=0.0,
        wait_known=False,
        max_seconds=max_time,
        detail=detail,
    )


def stamina_policy(decorator: ast.AST) -> RetryPolicy | None:
    call = _call_of(decorator)
    if call is None:
        return None
    name = dotted_name(call.func) or ""
    if not (name.startswith("stamina.") and _last(name) in {"retry", "retry_context"}):
        return None
    attempts_node = kwarg(call, "attempts")
    attempts = STAMINA_DEFAULT_ATTEMPTS
    detail = "stamina default attempts=10"
    if attempts_node is not None:
        value = number(attempts_node)
        if value is None:
            return RetryPolicy(
                source="stamina",
                attempts=STAMINA_DEFAULT_ATTEMPTS,
                attempts_known=False,
                backoff=True,
                detail="attempts= is not a literal",
            )
        attempts = value if value else UNBOUNDED
        detail = f"attempts={ast.unparse(attempts_node)}"
    timeout_node = kwarg(call, "timeout")
    max_seconds = STAMINA_DEFAULT_TIMEOUT if timeout_node is None else number(timeout_node)
    return RetryPolicy(
        source="stamina",
        attempts=attempts,
        backoff=True,
        wait_known=False,
        max_seconds=max_seconds,
        detail=detail,
    )


def celery_policy(decorator: ast.AST) -> RetryPolicy | None:
    call = _call_of(decorator)
    if call is None:
        return None
    name = dotted_name(call.func) or ""
    if _last(name) not in {"task", "shared_task"}:
        return None
    autoretry = kwarg(call, "autoretry_for")
    retry_kwargs = kwarg(call, "retry_kwargs")
    if autoretry is None and retry_kwargs is None:
        return None
    max_retries = number(kwarg(call, "max_retries"))
    if max_retries is None and isinstance(retry_kwargs, ast.Dict):
        for key, value in zip(retry_kwargs.keys, retry_kwargs.values):
            if isinstance(key, ast.Constant) and key.value == "max_retries":
                max_retries = number(value)
    if max_retries is None:
        max_retries = CELERY_DEFAULT_MAX_RETRIES
        detail = "celery default max_retries=3"
    else:
        detail = f"max_retries={int(max_retries)}"
    backoff_on = kwarg(call, "retry_backoff") is not None
    return RetryPolicy(
        source="celery",
        attempts=max_retries + 1,
        backoff=backoff_on,
        wait_known=False,
        detail=detail,
    )


DECORATOR_DETECTORS = (tenacity_policy, backoff_policy, stamina_policy, celery_policy)


def decorator_policy(decorator: ast.AST) -> RetryPolicy | None:
    for detector in DECORATOR_DETECTORS:
        policy = detector(decorator)
        if policy is not None:
            return policy
    return None


# --------------------------------------------------------------------------
# transport-level retries (urllib3 / requests / httpx)
# --------------------------------------------------------------------------


def _urllib3_wait_total(retries: float, factor: float, backoff_max: float) -> float:
    """Sum urllib3's backoff sleeps: factor * 2**(n-1) before retry n, none before the first."""
    if not math.isfinite(retries):
        return math.inf
    total = 0.0
    for attempt in range(2, int(retries) + 1):
        total += min(factor * (2 ** (attempt - 1)), backoff_max)
    return total


def urllib3_retry_policy(call: ast.Call) -> RetryPolicy | None:
    name = dotted_name(call.func) or ""
    if _last(name) != "Retry":
        return None
    total = number(kwarg(call, "total"))
    if total is None and call.args:
        total = number(call.args[0])
    if total is None:
        parts = [number(kwarg(call, key)) for key in ("connect", "read", "status", "other")]
        parts = [value for value in parts if value is not None]
        total = max(parts) if parts else URLLIB3_DEFAULT_TOTAL
        detail = "urllib3 Retry without total= (default total=10)" if not parts else "from connect/read/status"
    else:
        detail = f"Retry(total={int(total)})"
    factor = number(kwarg(call, "backoff_factor")) or 0.0
    backoff_max = number(kwarg(call, "backoff_max")) or URLLIB3_DEFAULT_BACKOFF_MAX
    return RetryPolicy(
        source="urllib3",
        attempts=total + 1,
        backoff=factor > 0,
        wait_total=_urllib3_wait_total(total, factor, backoff_max),
        max_seconds=None,
        detail=detail,
    )


def transport_policy(call: ast.Call) -> RetryPolicy | None:
    """Retries configured on an HTTP transport/adapter/session object."""
    policy = urllib3_retry_policy(call)
    if policy is not None:
        return policy
    name = _last(dotted_name(call.func) or "")
    if name == "HTTPAdapter":
        node = kwarg(call, "max_retries")
        if node is None:
            return None
        if isinstance(node, ast.Call):
            return urllib3_retry_policy(node)
        value = number(node)
        if value is None:
            return None
        return RetryPolicy(
            source="requests",
            attempts=value + 1,
            backoff=False,
            detail=f"HTTPAdapter(max_retries={int(value)}) retries connection errors",
        )
    if name in {"HTTPTransport", "AsyncHTTPTransport"}:
        value = number(kwarg(call, "retries"))
        if value is None:
            return None
        return RetryPolicy(
            source="httpx",
            attempts=value + 1,
            backoff=False,
            detail=f"httpx transport retries={int(value)} (connection errors)",
        )
    return None


# --------------------------------------------------------------------------
# timeouts and blocking calls
# --------------------------------------------------------------------------


def timeout_seconds(call: ast.Call) -> tuple[float, bool]:
    """Return (seconds, known) for a call's timeout= argument."""
    node = kwarg(call, "timeout")
    if node is None:
        return UNBOUNDED, True
    value = literal(node)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value), True
    if isinstance(value, tuple):
        numbers = [float(item) for item in value if isinstance(item, (int, float))]
        if numbers:
            return sum(numbers), True
    if isinstance(node, ast.Call):
        parts = [number(arg) for arg in node.args]
        parts += [number(keyword.value) for keyword in node.keywords]
        parts = [value for value in parts if value is not None]
        if parts:
            return max(parts), True
    return UNBOUNDED, False


def sleep_seconds(call: ast.Call) -> tuple[float, bool]:
    if call.args:
        value = number(call.args[0])
        if value is not None:
            return value, True
    return 0.0, False


def is_http_module_call(name: str) -> bool:
    head, _, tail = name.rpartition(".")
    if tail not in HTTP_METHODS:
        return False
    return head.split(".")[-1] in {"requests", "httpx", "aiohttp"}


def is_urlopen(name: str) -> bool:
    return name in {"urlopen", "urllib.request.urlopen", "request.urlopen"}


def is_subprocess(name: str) -> bool:
    head, _, tail = name.rpartition(".")
    return head.split(".")[-1] == "subprocess" and tail in {
        "run",
        "call",
        "check_call",
        "check_output",
        "communicate",
    }


def is_sleep(name: str) -> bool:
    return name in {"time.sleep", "sleep", "asyncio.sleep", "anyio.sleep", "trio.sleep"}


def is_socket_connect(name: str) -> bool:
    tail = name.rsplit(".", 1)[-1]
    return tail in {"create_connection", "connect"} and "socket" in name


def wait_for_deadline(call: ast.Call) -> float | None:
    """asyncio.wait_for(coro, timeout) imposes a deadline on everything inside."""
    name = dotted_name(call.func) or ""
    if _last(name) not in {"wait_for", "timeout"} or "asyncio" not in name:
        return None
    if _last(name) == "wait_for":
        node = kwarg(call, "timeout")
        if node is None and len(call.args) > 1:
            node = call.args[1]
    else:
        node = call.args[0] if call.args else kwarg(call, "delay")
    return number(node)
