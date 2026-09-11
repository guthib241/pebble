# backfire

Finds retry amplification and timeout blowups in Python codebases.

Retries multiply when they are stacked. A handler that retries three times, calling a
service that retries twice, calling an HTTP client configured with `Retry(total=4)`,
sends **30** requests for one logical call. Each layer looks reasonable on its own, and
no single file shows the product. `backfire` reads the whole project, resolves the call
graph, and multiplies the retry policies it finds along each path.

```
$ backfire tests/fixtures/layered
client.py:15: WARNING BF001 (retry amplification): self.session.get() can run up to 30 times
through composed retries via api.handle_request -> service.UserService.fetch -> client.ApiClient.get_user
    via api.py:8 tenacity decorator: 3 attempts
    via service.py:13 loop: 2 attempts
    via client.py:15 urllib3 transport: 5 attempts (Retry(total=4))
```

## Closest prior art

**Closest prior art:** Semgrep's Python rules (for example
[`python.requests.best-practice.use-timeout`](https://github.com/semgrep/semgrep-rules/blob/develop/python/requests/best-practice/use-timeout.yaml))
for single-call retry and timeout checks; [Retry Storm Lab](https://github.com/telemetry-sh/retry-storm-lab)
for retry-policy behaviour; the arXiv study *Retry Amplification in Distributed Systems*
(arXiv:2608.25403), which used regex-based static detection of retry libraries to measure
how common retry logic is across repositories.

**Difference:** those match or measure one retry site at a time, or simulate a policy in
the abstract. `backfire` composes the sites: it resolves calls between functions, classes
and modules in the project, multiplies the attempt counts along each path, and reports the
worst-case attempt count and wall-clock time for a single logical call, with the
contributing retry sites named.

**Search confidence:** Medium.

**Scope:** This assessment reflects the sources and queries documented in
[`NOVELTY_REPORT.md`](NOVELTY_REPORT.md). It is not a claim that nothing similar exists.

## Status

Working and tested on real projects. Version 0.1.0. Python 3.11+, no runtime dependencies.
It analyzes Python source only; retry policies configured in YAML, service meshes or
infrastructure config are outside its scope.

## Install

```bash
git clone https://github.com/guthib241/backfire
cd backfire
pip install .
```

Or run it from a checkout without installing:

```bash
python -m backfire path/to/project
```

## Usage

```bash
backfire src/                          # scan a directory
backfire src/ --max-attempts 6         # report anything above 6 composed attempts
backfire src/ --budget "api.handler=10s"   # flag paths whose worst case exceeds a budget
backfire src/ --json                   # machine-readable output
backfire src/ --fail-on warning        # CI gate
```

Exit codes: `0` clean, `1` findings at or above `--fail-on` (default `error`), `2` usage error.

Silence a finding with a comment on the reported line:

```python
while True:  # backfire: ignore[BF002]
```

Optional configuration, in `backfire.toml` or under `[tool.backfire]` in `pyproject.toml`:

```toml
max_attempts = 8
exclude = ["migrations"]

[budgets]
"api.handle_request" = "10s"
```

## What it reports

| Rule | Meaning |
| --- | --- |
| BF001 | A call is reachable with more composed attempts than the threshold |
| BF002 | A retry declares no attempt cap and no time cap |
| BF003 | A retry repeats with no backoff anywhere in the retried code |
| BF004 | A blocking call with no timeout sits under a retry |
| BF005 | Worst-case time exceeds a declared budget or an `asyncio.wait_for` deadline |

### Retry mechanisms it recognises

- `tenacity` (`@retry`, stop and wait policies, including `|`-combined stops)
- `backoff` (`@backoff.on_exception`, `@backoff.on_predicate`)
- `stamina` (`@stamina.retry`, including its documented defaults)
- Celery tasks with `autoretry_for` / `retry_kwargs`
- `urllib3.Retry`, `requests` `HTTPAdapter(max_retries=...)` mounted on a session
- `httpx.HTTPTransport(retries=...)`
- Hand-rolled loops: `for _ in range(n)` and `while True` around a `try`/`except`

Blocking calls it costs: `requests`/`httpx`/`aiohttp` methods, `urlopen`, socket connects,
`subprocess` calls, and `time`/`asyncio`/`anyio`/`trio` sleeps.

## How the numbers are computed

- An attempt count includes the first attempt: `Retry(total=4)` is 5 attempts.
- Composed attempts are the product of every retry scope on the path — decorators, the
  loops containing the call site, and the transport the client was built with.
- Worst-case time assumes every call in a body runs on every attempt, each blocking call
  takes its full declared timeout, and backoff waits are their documented maximum. It is
  an upper bound, not a prediction.
- A retry whose attempt count is not a literal (a computed expression, a value from
  settings) is estimated at 3 attempts and the finding says it is an estimate. Module-level
  constants (`MAX_TRIES = 5`) are resolved and are not estimates.

## Limitations

These are the failure modes observed while testing against real projects.

- **Static call graph.** Calls are resolved through imports, `self.method()`, base classes,
  and variables assigned from a constructor. Calls through dependency injection, callables
  stored in dicts, or dynamic dispatch are not resolved, so real paths can be missed.
  `--resolve-by-name` adds edges for uniquely-named functions at the cost of precision.
- **Retries configured outside Python.** Service-mesh retry policies, YAML-configured
  clients and gateway retries are invisible to it, so the real product can be higher.
- **BF002 flags any unbounded retry loop**, including event-consumer loops and interactive
  re-prompt loops, where looping forever is the design. In the PrefectHQ/prefect run below,
  most BF002 findings are loops of that kind.
- **Unrecognised clients.** Database drivers, boto3, Kafka clients and similar are not
  costed as blocking calls, so their timeouts do not appear in worst-case time.
- Nested functions are analyzed, but a call to a nested function by bare name is not
  resolved back to it.

## Validation

Test suite: 85 tests covering policy extraction for each supported library, loop
recognition (including loops that must *not* be treated as retries), call-graph
resolution, the amplification and duration arithmetic, config parsing, and CLI exit codes.

```bash
pip install -e ".[dev]"
pytest
```

The arithmetic is checked against hand-computed expectations in
`tests/test_analyze.py`: the layered fixture composes to 30 attempts (3 × 2 × 5) and a
199-second worst case, and the deadline fixture to 26 seconds (4 × 5s + 6s of waits).

### Runs on real projects

Environment: CPython 3.11.15, Linux x86_64 container. Command:
`python -m backfire <path> --json --fail-on none`, wall time is the best of three runs.

| Project | Commit | Files | Functions | Call edges | Retry sites | Findings | Time |
| --- | --- | --- | --- | --- | --- | --- | --- |
| backfire (itself) | this tree | 10 | 102 | 235 | 0 | 0 | 0.11s |
| psf/requests (`src`) | `dae7ef6` | 19 | 245 | 254 | 0 | 0 | 0.14s |
| openai/openai-python (`src`) | `d7c41ef` | 1840 | 3919 | 4716 | 14 | 0 | 1.66s |
| PrefectHQ/prefect (`src`) | `d82220b` | 1268 | 12746 | 10191 | 41 | 29 | 5.46s |

The prefect findings are 22 BF002, 6 BF003 and 1 BF004; none of its retry sites compose
above the default threshold of 10 attempts. Two projects producing zero findings is the
control: requests and openai-python both configure retries in a single layer, and a tool
that reported amplification there would be wrong.

Determinism control: two consecutive runs over PrefectHQ/prefect produced byte-identical
JSON output.

No comparison against another tool is made here, because no tool with the same output was
found to compare against.

## License

This project is released under the license in [`LICENSE.txt`](LICENSE.txt): a custom
attribution, non-commercial license, chosen because the author requires visible credit and
wants commercial use negotiated separately rather than granted by default. It is
source-available, not an OSI-approved open-source license. Commercial use requires written
permission from the author.
