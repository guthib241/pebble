"""Known unit conventions of standard library and very widely used callables.

Each entry records the units a callable expects for its parameters and the unit of
its return value. Parameters are keyed by name and, where a call is normally
written positionally, also by zero-based position.

Only conventions that are documented and stable are listed here. Third-party
entries are limited to ``requests``, whose ``timeout`` argument is in seconds.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Union

from .units import LEXICON, Unit

SECONDS = LEXICON["seconds"]
MILLISECONDS = LEXICON["milliseconds"]
NANOSECONDS = LEXICON["nanoseconds"]
BYTES = LEXICON["bytes"]
RADIANS = LEXICON["radians"]
DEGREES = LEXICON["degrees"]


@dataclass(frozen=True)
class KnownSignature:
    """Units for a callable's parameters and return value."""

    params: Dict[Union[str, int], Unit] = field(default_factory=dict)
    returns: Optional[Unit] = None


def _timeout_seconds(*positions: int) -> KnownSignature:
    params: Dict[Union[str, int], Unit] = {"timeout": SECONDS}
    for position in positions:
        params[position] = SECONDS
    return KnownSignature(params=params)


#: Callables addressed by their dotted import path.
FUNCTIONS: Dict[str, KnownSignature] = {
    # time
    "time.sleep": KnownSignature(params={0: SECONDS, "secs": SECONDS}),
    "time.time": KnownSignature(returns=SECONDS),
    "time.monotonic": KnownSignature(returns=SECONDS),
    "time.perf_counter": KnownSignature(returns=SECONDS),
    "time.process_time": KnownSignature(returns=SECONDS),
    "time.thread_time": KnownSignature(returns=SECONDS),
    "time.time_ns": KnownSignature(returns=NANOSECONDS),
    "time.monotonic_ns": KnownSignature(returns=NANOSECONDS),
    "time.perf_counter_ns": KnownSignature(returns=NANOSECONDS),
    "time.process_time_ns": KnownSignature(returns=NANOSECONDS),
    # asyncio
    "asyncio.sleep": KnownSignature(params={0: SECONDS, "delay": SECONDS}),
    "asyncio.wait_for": KnownSignature(params={1: SECONDS, "timeout": SECONDS}),
    "asyncio.wait": _timeout_seconds(),
    "asyncio.timeout": KnownSignature(params={0: SECONDS, "delay": SECONDS}),
    "asyncio.timeout_at": KnownSignature(params={0: SECONDS, "when": SECONDS}),
    # sockets and io waiting
    "socket.setdefaulttimeout": KnownSignature(params={0: SECONDS}),
    "socket.getdefaulttimeout": KnownSignature(returns=SECONDS),
    "select.select": KnownSignature(params={3: SECONDS, "timeout": SECONDS}),
    "select.poll.poll": KnownSignature(params={0: MILLISECONDS, "timeout": MILLISECONDS}),
    "signal.alarm": KnownSignature(params={0: SECONDS, "time": SECONDS}),
    "signal.setitimer": KnownSignature(params={1: SECONDS, "seconds": SECONDS}),
    # subprocess
    "subprocess.run": _timeout_seconds(),
    "subprocess.call": _timeout_seconds(),
    "subprocess.check_call": _timeout_seconds(),
    "subprocess.check_output": _timeout_seconds(),
    # urllib and requests
    "urllib.request.urlopen": KnownSignature(params={2: SECONDS, "timeout": SECONDS}),
    "requests.get": _timeout_seconds(),
    "requests.post": _timeout_seconds(),
    "requests.put": _timeout_seconds(),
    "requests.patch": _timeout_seconds(),
    "requests.delete": _timeout_seconds(),
    "requests.head": _timeout_seconds(),
    "requests.request": _timeout_seconds(),
    # sizes
    "os.path.getsize": KnownSignature(returns=BYTES),
    "os.get_terminal_size": KnownSignature(),
    "os.truncate": KnownSignature(params={1: BYTES, "length": BYTES}),
    "os.read": KnownSignature(params={1: BYTES, "n": BYTES}),
    "bytearray": KnownSignature(params={0: BYTES}),
    # angles: the math module works in radians
    "math.sin": KnownSignature(params={0: RADIANS, "x": RADIANS}),
    "math.cos": KnownSignature(params={0: RADIANS, "x": RADIANS}),
    "math.tan": KnownSignature(params={0: RADIANS, "x": RADIANS}),
    "math.asin": KnownSignature(returns=RADIANS),
    "math.acos": KnownSignature(returns=RADIANS),
    "math.atan": KnownSignature(returns=RADIANS),
    "math.atan2": KnownSignature(returns=RADIANS),
    "math.radians": KnownSignature(params={0: DEGREES, "x": DEGREES}, returns=RADIANS),
    "math.degrees": KnownSignature(params={0: RADIANS, "x": RADIANS}, returns=DEGREES),
}

#: Callables addressed by attribute name alone, for calls on objects whose type is
#: not resolved (``sock.settimeout(...)``). Restricted to names whose unit meaning
#: does not vary in practice.
METHODS: Dict[str, KnownSignature] = {
    "settimeout": KnownSignature(params={0: SECONDS, "value": SECONDS}),
    "gettimeout": KnownSignature(returns=SECONDS),
    "total_seconds": KnownSignature(returns=SECONDS),
    "recv": KnownSignature(params={0: BYTES, "bufsize": BYTES}),
    "recv_into": KnownSignature(params={1: BYTES, "nbytes": BYTES}),
    "timestamp": KnownSignature(returns=SECONDS),
}

#: Attributes whose unit is known regardless of the object they are read from.
ATTRIBUTES: Dict[str, Unit] = {
    "st_size": BYTES,
}

#: Calls that return their first argument's unit unchanged.
PASSTHROUGH_CALLS = frozenset({"int", "float", "round", "abs", "math.floor", "math.ceil",
                               "math.fabs", "math.trunc"})

#: Calls whose arguments must share a unit and which return that unit.
UNIFYING_CALLS = frozenset({"min", "max"})

#: Names of constants whose numeric value is known.
CONSTANTS: Dict[str, float] = {
    "math.pi": 3.141592653589793,
    "math.tau": 6.283185307179586,
    "math.e": 2.718281828459045,
}
