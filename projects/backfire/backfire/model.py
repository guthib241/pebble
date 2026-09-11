"""Data model shared by the parser, resolver and analyzer."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

UNBOUNDED = math.inf


@dataclass(frozen=True, order=True)
class Location:
    file: str
    line: int

    def __str__(self) -> str:
        return f"{self.file}:{self.line}"


@dataclass
class RetryPolicy:
    """A retry configuration found in source.

    ``attempts`` counts total attempts including the first one, so a policy
    that retries twice after an initial failure has ``attempts == 3``.
    ``math.inf`` means the policy declares no attempt cap.
    """

    source: str
    attempts: float
    attempts_known: bool = True
    backoff: bool = False
    wait_total: float = 0.0
    wait_known: bool = True
    max_seconds: float | None = None
    detail: str = ""

    @property
    def unbounded(self) -> bool:
        return math.isinf(self.attempts) and self.max_seconds is None


@dataclass
class RetrySite:
    policy: RetryPolicy
    location: Location
    kind: str  # "decorator" | "loop" | "transport"
    start_line: int = 0
    end_line: int = 0

    def describe(self) -> str:
        attempts = "unbounded" if math.isinf(self.policy.attempts) else f"{int(self.policy.attempts)} attempts"
        label = self.policy.source if self.policy.source == self.kind else f"{self.policy.source} {self.kind}"
        return f"{self.location} {label}: {attempts}"


@dataclass
class BlockingCall:
    location: Location
    kind: str  # "http" | "socket" | "subprocess" | "sleep"
    timeout: float
    timeout_known: bool
    detail: str
    scopes: tuple[int, ...] = ()
    transport: RetryPolicy | None = None


@dataclass
class CallSite:
    raw: str
    location: Location
    scopes: tuple[int, ...] = ()
    target: str | None = None
    hint: str | None = None


@dataclass
class Deadline:
    seconds: float
    location: Location
    start_line: int
    end_line: int
    detail: str = ""
    handled: bool = False  # the caller catches TimeoutError, so firing is intentional


@dataclass
class FunctionInfo:
    qualname: str
    location: Location
    module: str
    cls: str | None
    is_async: bool = False
    entry_sites: list[RetrySite] = field(default_factory=list)
    block_scopes: list[RetrySite] = field(default_factory=list)
    calls: list[CallSite] = field(default_factory=list)
    blocking: list[BlockingCall] = field(default_factory=list)
    deadlines: list[Deadline] = field(default_factory=list)

    @property
    def short(self) -> str:
        return self.qualname.split(":", 1)[-1]


@dataclass
class ClassInfo:
    name: str
    module: str
    bases: list[str] = field(default_factory=list)
    attr_types: dict[str, str] = field(default_factory=dict)
    attr_transports: dict[str, RetryPolicy] = field(default_factory=dict)
    attr_timeouts: dict[str, float] = field(default_factory=dict)
    methods: dict[str, str] = field(default_factory=dict)

    @property
    def qualname(self) -> str:
        return f"{self.module}.{self.name}"


@dataclass
class ModuleInfo:
    name: str
    path: str
    imports: dict[str, str] = field(default_factory=dict)
    functions: dict[str, FunctionInfo] = field(default_factory=dict)
    classes: dict[str, ClassInfo] = field(default_factory=dict)
    parse_error: str | None = None
    suppressions: dict[int, set[str] | None] = field(default_factory=dict)


@dataclass
class Finding:
    rule: str
    severity: str  # "error" | "warning" | "info"
    message: str
    location: Location
    evidence: list[str] = field(default_factory=list)
    data: dict = field(default_factory=dict)

    def sort_key(self) -> tuple:
        rank = {"error": 0, "warning": 1, "info": 2}.get(self.severity, 3)
        weight = -float(self.data.get("attempts", 0) or 0)
        if math.isinf(weight):
            weight = -1e18
        return (rank, weight, self.location.file, self.location.line, self.rule)


SEVERITY_ORDER = {"info": 0, "warning": 1, "error": 2}
