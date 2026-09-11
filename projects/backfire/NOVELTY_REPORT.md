# Novelty report: backfire

**Project:** backfire
**Description:** A static analyzer that multiplies retry policies along a Python project's
call graph and reports the worst-case attempts and wall-clock time for one logical call.
**Date of search:** 2026-09-11
**Conclusion:** No materially equivalent implementation was found within the documented
search scope. **Novelty confidence: Medium.**

This conclusion is limited to the sources and queries below. It is not a claim that no
such tool exists anywhere.

## Search scope

Searched:

- Public source repositories (GitHub repository search via the GitHub API).
- Package registries: PyPI (name lookups), npm (name lookups).
- Web search across engineering blogs, documentation and forums (September 2026 index).
- Academic material surfaced through web search (arXiv results; see the gap below).
- Issue trackers and discussion threads surfaced through web search (istio/istio issues,
  Lobsters, Medium/DEV engineering posts).

Not searched: paywalled digital libraries (ACM, IEEE), Google Scholar directly, private or
internal tooling, non-English sources.

## Queries used

Candidate that was rejected first (see below):

1. `crontab linter static analysis tool detect DST daylight saving cron schedule problems`
2. `cron lint tool day-of-month day-of-week OR semantics footgun percent sign escaping crontab checker`
3. GitHub repository search: `crontab lint linter`
4. PyPI lookups: `cronlint`, `cron-lint`, `crontab-lint`, `croniter`, `cron-descriptor`, `crondst`

Selected candidate:

5. `static analysis tool detect nested retries retry amplification retry storm linter source code`
6. `tool analyze timeout budget call graph inner timeout larger than outer timeout detection microservices code`
7. `"retry amplification" OR "nested retry" detection tool github static analyzer python codebase`
8. `"retry" static analysis detect anti-patterns research tool "call graph" multiplication attempts paper artifact`
9. `semgrep rules retry without backoff missing timeout requests python registry resilience linter`
10. `how to find nested retries in codebase stackoverflow "retries multiply" total attempts layered clients question`
11. `resilience4j OR istio OR envoy retry budget static configuration analyzer lint tool detect multiplied retries java go`
12. GitHub repository search: `retry linter static analysis retries`
13. GitHub repository search: `retry budget analyzer timeout inversion` (0 results)
14. PyPI lookups: `retrylint`, `retry-lint`, `retryscope`, `retry-analyzer`; npm lookups: `retry-lint`, `retrylint`

## The rejected candidate

The first candidate was a crontab linter that would flag DST hazards, day-of-month /
day-of-week OR-semantics traps, unescaped `%`, and schedules that never fire. Searches 1-4
found materially equivalent tools already published:

- [SNO7E-G/CronLens](https://github.com/SNO7E-G/CronLens) — "Translate, schedule and lint
  cron expressions in your terminal, with DST, overlap and thundering-herd warnings."
- [HeytalePazguato/cron-doctor](https://github.com/HeytalePazguato/cron-doctor) — "Audit
  your crontab in seconds. Plain-English schedule explanations, ten lint checks, calendar
  view, JSON output."
- [zbcdo/cronlint](https://github.com/zbcdo/cronlint) — "catches the schedule bugs that
  syntax checkers can't."

Same problem, same user, same workflow, same deployment model. The candidate was rejected
under the material-equivalence test rather than reframed.

## Closest prior art for backfire

### 1. Semgrep rules for retry and timeout patterns

[`semgrep-rules`](https://github.com/semgrep/semgrep-rules/blob/develop/python/requests/best-practice/use-timeout.yaml),
e.g. `python.requests.best-practice.use-timeout`. Pattern-matches a single call site and
reports a missing `timeout=`.

### 2. Retry Storm Lab

[telemetry-sh/retry-storm-lab](https://github.com/telemetry-sh/retry-storm-lab). Inspected
directly: a deterministic queueing simulator that models fresh requests and retries during
a capacity failure and compares backoff policies. It does not read a codebase.

### 3. arXiv:2608.25403, *Retry Amplification in Distributed Systems*

A study that used regex-based static detection of retry constructs (`@retry`, tenacity,
backoff, `urllib3.Retry`) across 200 Python repositories to measure how often retry logic
appears, and reports its own false-negative rate for hand-rolled loops. **Search gap:**
arxiv.org and semanticscholar.org are blocked by this environment's network egress policy,
so this paper is known only through search-result summaries, not from reading it. If that
work released a reusable analyzer that composes retries along a call graph, this report's
confidence would be too high. That single unresolved item is the main reason the rating is
Medium rather than High.

### 4. Service-mesh retry budgets (Envoy, Istio, Gateway API GEP-3388)

Runtime configuration that caps concurrent retries at a proxy. Configuration, not source
analysis, and it does not see application-level retry loops.

## Feature comparison

| Dimension | backfire | Semgrep rules | Retry Storm Lab | arXiv:2608.25403 | Envoy/Istio retry budgets |
| --- | --- | --- | --- | --- | --- |
| Problem | Composed retry blow-up in one codebase | Single risky call site | Policy dynamics under load | Prevalence of retry logic | Limit retries in flight |
| User | Developer or SRE reviewing a service | Developer | Engineer studying policies | Researcher | Platform operator |
| Input | A Python project | One file at a time | Simulation parameters | A repository corpus | Mesh configuration |
| Mechanism | Call graph + product of attempt counts | AST pattern match | Queueing simulation | Regex detection, counted | Proxy runtime counters |
| Output | Worst-case attempts and time per path, with each contributing site | Match locations | Simulated curves | Statistics over a corpus | Rejected retries at runtime |
| Cross-function | Yes | No | Not applicable | No | Not applicable |
| Deployment | CLI, CI gate | CLI, CI gate | Interactive tool | Paper | Production infrastructure |

## Distinguishing capability

Composition across layers. Every piece backfire uses (AST parsing, call-graph
construction, recognising `tenacity`) is ordinary; what the search did not turn up is a
tool that multiplies those retry policies along resolved call paths and reports the product
for a single logical call, together with the worst-case wall-clock time and the specific
sites that produced it. The engineering advice found repeatedly in the search — "audit your
layers, coordinate your retry budgets" — is given as manual work, which is the gap this
fills.

## Unresolved uncertainty

- arXiv:2608.25403 could not be read directly (egress blocked). Its artifacts, if any, are
  unverified.
- Paywalled academic databases were not searched; a research prototype may exist there.
- Similar tooling may exist inside companies or in repositories that rank poorly for the
  terms used here.
- Java, Go and .NET ecosystems were searched only through general web queries; a composed
  retry analyzer for another language would be close prior art in mechanism, though
  different in ecosystem.

## Licence note

The project ships under the repository owner's custom attribution, non-commercial license
(`LICENSE.txt`), chosen because the author requires visible credit and wants commercial use
negotiated rather than granted by default. It is source-available, not OSI open source.
