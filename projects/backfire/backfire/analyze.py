"""Compose retry policies along the call graph and produce findings."""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .graph import CallGraph
from .model import BlockingCall, Finding, FunctionInfo, Location, RetrySite

DEFAULT_MAX_ATTEMPTS = 10.0
DEFAULT_MAX_DEPTH = 12
DEFAULT_MAX_PATHS = 20000


@dataclass
class Amplification:
    attempts: float
    duration: float
    known: bool
    path: list[str]
    function: str
    call: BlockingCall
    evidence: list[str] = field(default_factory=list)

    @property
    def location(self) -> Location:
        return self.call.location


@dataclass
class Options:
    max_attempts: float = DEFAULT_MAX_ATTEMPTS
    max_depth: int = DEFAULT_MAX_DEPTH
    max_paths: int = DEFAULT_MAX_PATHS
    budgets: dict[str, float] = field(default_factory=dict)
    default_budget: float | None = None


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    amplifications: list[Amplification] = field(default_factory=list)
    stats: dict = field(default_factory=dict)


def entry_attempts(function: FunctionInfo) -> float:
    total = 1.0
    for site in function.entry_sites:
        total *= site.policy.attempts
    return total


def entry_wait(function: FunctionInfo) -> float:
    return sum(site.policy.wait_total for site in function.entry_sites)


def scope_multiplier(function: FunctionInfo, scopes: tuple[int, ...]) -> float:
    total = 1.0
    for index in scopes:
        total *= function.block_scopes[index].policy.attempts
    return total


def _all_known(sites) -> bool:
    return all(site.policy.attempts_known for site in sites)


def _scope_sites(function: FunctionInfo, scopes: tuple[int, ...]) -> list[RetrySite]:
    return [function.block_scopes[index] for index in scopes]


def _blocking_cost(call: BlockingCall) -> float:
    """Worst-case seconds one execution of this call can block for."""
    if call.kind == "sleep":
        return call.timeout
    seconds = call.timeout
    if call.transport is not None:
        attempts = call.transport.attempts
        seconds = seconds * attempts + call.transport.wait_total
    return seconds


class Analyzer:
    def __init__(self, graph: CallGraph, options: Options | None = None):
        self.graph = graph
        self.options = options or Options()
        self._cost_memo: dict[str, float] = {}
        self.expansions = 0

    # -- cost ------------------------------------------------------------
    def function_cost(self, qualname: str, stack: tuple[str, ...] = ()) -> float:
        if qualname in stack:
            frames = [self.graph.functions[name] for name in stack if name in self.graph.functions]
            return math.inf if any(entry_attempts(item) > 1 for item in frames) else 0.0
        if qualname in self._cost_memo:
            return self._cost_memo[qualname]
        function = self.graph.functions.get(qualname)
        if function is None:
            return 0.0
        body = 0.0
        for call in function.blocking:
            body += scope_multiplier(function, call.scopes) * _blocking_cost(call)
        # Loop-level waits are counted through the sleep calls inside the loop;
        # this only adds waits a policy declares itself (library-internal sleeps).
        body += sum(site.policy.wait_total for site in function.block_scopes)
        for call, target in self.graph.edges.get(qualname, []):
            body += scope_multiplier(function, call.scopes) * self.function_cost(target, stack + (qualname,))
        total = entry_attempts(function) * body + entry_wait(function)
        if not stack:
            self._cost_memo[qualname] = total
        return total

    def subtree_cost(self, function: FunctionInfo, start: int, end: int) -> float:
        """Worst-case seconds for the work between two source lines of a function."""
        total = 0.0
        for call in function.blocking:
            if start <= call.location.line <= end:
                total += scope_multiplier(function, call.scopes) * _blocking_cost(call)
        for call, target in self.graph.edges.get(function.qualname, []):
            if start <= call.location.line <= end:
                total += scope_multiplier(function, call.scopes) * self.function_cost(target)
        return total

    # -- amplification ---------------------------------------------------
    def amplifications(self) -> list[Amplification]:
        best: dict[tuple[str, int], Amplification] = {}
        roots = self.graph.roots() or sorted(self.graph.functions)
        for root in roots:
            self._walk(root, 1.0, [root], [], True, best, 0)
        return sorted(best.values(), key=lambda item: (-item.attempts, str(item.location)))

    def _walk(self, qualname, multiplier, path, evidence, known, best, depth):
        if depth > self.options.max_depth or self.expansions > self.options.max_paths:
            return
        self.expansions += 1
        function = self.graph.functions.get(qualname)
        if function is None:
            return
        here = multiplier * entry_attempts(function)
        here_known = known and _all_known(function.entry_sites)
        local_evidence = evidence + [site.describe() for site in function.entry_sites]

        for call in function.blocking:
            if call.kind == "sleep":
                continue
            scopes = _scope_sites(function, call.scopes)
            attempts = here * scope_multiplier(function, call.scopes)
            transport_evidence: list[str] = []
            if call.transport is not None:
                attempts *= call.transport.attempts
                transport_evidence.append(
                    f"{call.location} {call.transport.source} transport: "
                    f"{int(call.transport.attempts)} attempts ({call.transport.detail})"
                )
            record = Amplification(
                attempts=attempts,
                duration=attempts * call.timeout,
                known=here_known and _all_known(scopes),
                path=list(path),
                function=qualname,
                call=call,
                evidence=local_evidence
                + [site.describe() for site in scopes]
                + transport_evidence,
            )
            key = (call.location.file, call.location.line)
            current = best.get(key)
            if current is None or record.attempts > current.attempts:
                best[key] = record

        for call, target in self.graph.edges.get(qualname, []):
            if target in path:
                continue
            scopes = _scope_sites(function, call.scopes)
            self._walk(
                target,
                here * scope_multiplier(function, call.scopes),
                path + [target],
                local_evidence + [site.describe() for site in scopes],
                here_known and _all_known(scopes),
                best,
                depth + 1,
            )

    # -- findings --------------------------------------------------------
    def run(self) -> Report:
        report = Report()
        records = self.amplifications()
        report.amplifications = records
        report.findings.extend(self._amplification_findings(records))
        report.findings.extend(self._policy_findings())
        report.findings.extend(self._timeout_findings(records))
        report.findings.extend(self._budget_findings())
        report.findings.sort(key=lambda finding: finding.sort_key())
        report.stats = {
            "functions": len(self.graph.functions),
            "edges": sum(len(items) for items in self.graph.edges.values()),
            "resolved_calls": self.graph.resolved,
            "unresolved_calls": self.graph.unresolved,
            "retry_sites": sum(
                len(function.entry_sites)
                + len(function.block_scopes)
                + sum(1 for call in function.blocking if call.transport is not None)
                for function in self.graph.functions.values()
            ),
        }
        return report

    def _amplification_findings(self, records) -> list[Finding]:
        findings = []
        for record in records:
            if record.attempts <= self.options.max_attempts:
                continue
            if math.isinf(record.attempts):
                severity = "error"
                attempts_text = "an unbounded number of"
            else:
                severity = "error" if record.attempts > self.options.max_attempts * 3 else "warning"
                attempts_text = f"up to {int(record.attempts)}"
            hops = " -> ".join(_short(name) for name in record.path)
            estimate = "" if record.known else " (estimated: some attempt counts are not literals)"
            findings.append(
                Finding(
                    rule="BF001",
                    severity=severity,
                    message=(
                        f"{record.call.detail} can run {attempts_text} times through composed retries"
                        f" via {hops}{estimate}"
                    ),
                    location=record.location,
                    evidence=record.evidence,
                    data={
                        "attempts": record.attempts,
                        "path": record.path,
                        "known": record.known,
                        "call": record.call.detail,
                    },
                )
            )
        return findings

    def _function_sleeps(self, qualname: str, seen: frozenset = frozenset()) -> bool:
        if qualname in seen:
            return False
        function = self.graph.functions.get(qualname)
        if function is None:
            return False
        if any(call.kind == "sleep" for call in function.blocking):
            return True
        return any(
            self._function_sleeps(target, seen | {qualname})
            for _, target in self.graph.edges.get(qualname, [])
        )

    def _scope_sleeps(self, function: FunctionInfo, site: RetrySite) -> bool:
        """True when the retried code waits somewhere, directly or in a callee."""
        if site.kind == "decorator":
            start, end = 0, 10**9
        else:
            start, end = site.start_line, site.end_line
        for call in function.blocking:
            if call.kind == "sleep" and start <= call.location.line <= end:
                return True
        for call, target in self.graph.edges.get(function.qualname, []):
            if start <= call.location.line <= end and self._function_sleeps(
                target, frozenset({function.qualname})
            ):
                return True
        return False

    def _policy_findings(self) -> list[Finding]:
        findings = []
        for function in self.graph.functions.values():
            for site in list(function.entry_sites) + list(function.block_scopes):
                policy = site.policy
                if policy.unbounded and policy.attempts_known:
                    findings.append(
                        Finding(
                            rule="BF002",
                            severity="error" if not policy.backoff else "warning",
                            message=(
                                f"{policy.source} retry on {_short(function.qualname)} has no attempt cap"
                                f" and no time cap ({policy.detail})"
                            ),
                            location=site.location,
                            evidence=[site.describe()],
                            data={"attempts": math.inf, "source": policy.source},
                        )
                    )
                elif policy.attempts > 1 and not policy.backoff and not self._scope_sleeps(function, site):
                    estimate = "" if policy.attempts_known else " (estimated attempt count)"
                    findings.append(
                        Finding(
                            rule="BF003",
                            severity="warning",
                            message=(
                                f"{policy.source} retry on {_short(function.qualname)} retries"
                                f" {int(policy.attempts)} times with no backoff between attempts{estimate}"
                            ),
                            location=site.location,
                            evidence=[site.describe()],
                            data={"attempts": policy.attempts, "source": policy.source},
                        )
                    )
        return findings

    def _timeout_findings(self, records) -> list[Finding]:
        findings = []
        by_location = {(item.call.location.file, item.call.location.line): item for item in records}
        for function in self.graph.functions.values():
            for call in function.blocking:
                if call.kind == "sleep" or math.isfinite(call.timeout):
                    continue
                record = by_location.get((call.location.file, call.location.line))
                if record is not None:
                    attempts = record.attempts
                else:
                    attempts = entry_attempts(function) * scope_multiplier(function, call.scopes)
                    if call.transport is not None:
                        attempts *= call.transport.attempts
                if attempts <= 1:
                    continue
                reason = (
                    "is retried an unbounded number of times"
                    if math.isinf(attempts)
                    else f"is retried up to {int(attempts)} times"
                )
                findings.append(
                    Finding(
                        rule="BF004",
                        severity="error" if math.isinf(attempts) else "warning",
                        message=(
                            f"{call.detail} has no timeout and {reason}, so one failure can block forever"
                        ),
                        location=call.location,
                        evidence=record.evidence if record else [],
                        data={"attempts": attempts, "call": call.detail},
                    )
                )
        return findings

    def _budget_findings(self) -> list[Finding]:
        findings = []
        for function in self.graph.functions.values():
            for deadline in function.deadlines:
                if deadline.handled:
                    continue  # the timeout is caught, so hitting it is the design
                cost = self.subtree_cost(function, deadline.start_line, deadline.end_line)
                if cost <= deadline.seconds:
                    continue
                findings.append(
                    Finding(
                        rule="BF005",
                        severity="error",
                        message=(
                            f"work inside {deadline.detail}(timeout={_seconds(deadline.seconds)}) can take"
                            f" {_seconds(cost)} in the worst case, so the deadline fires before the retries finish"
                        ),
                        location=deadline.location,
                        evidence=[f"{deadline.location} deadline {_seconds(deadline.seconds)}"],
                        data={"budget": deadline.seconds, "worst_case": cost},
                    )
                )
        for qualname, budget in self.options.budgets.items():
            matches = [name for name in self.graph.functions if _matches(name, qualname)]
            for name in matches:
                cost = self.function_cost(name)
                if cost <= budget:
                    continue
                findings.append(
                    Finding(
                        rule="BF005",
                        severity="error",
                        message=(
                            f"{_short(name)} has a declared budget of {_seconds(budget)} but its worst-case"
                            f" retry path takes {_seconds(cost)}"
                        ),
                        location=self.graph.functions[name].location,
                        evidence=[f"budget {_seconds(budget)} declared for {qualname}"],
                        data={"budget": budget, "worst_case": cost},
                    )
                )
        return findings


def _matches(qualname: str, pattern: str) -> bool:
    if qualname == pattern:
        return True
    return qualname.endswith(f":{pattern}") or qualname.split(":", 1)[-1] == pattern


def _short(qualname: str) -> str:
    module, _, rest = qualname.partition(":")
    return f"{module.rsplit('.', 1)[-1]}.{rest}" if rest else qualname


def _seconds(value: float) -> str:
    if math.isinf(value):
        return "unbounded time"
    if value >= 60:
        return f"{value / 60:.1f}min"
    return f"{value:.1f}s"


def analyze(graph: CallGraph, options: Options | None = None) -> Report:
    return Analyzer(graph, options).run()
