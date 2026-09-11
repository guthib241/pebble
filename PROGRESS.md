# Progress

Status: one project complete; publication location deviates from AGENT_RULES (see blocker)
Current project: backfire (`projects/backfire/`)
Last run: 2026-09-11

## What happened this run

1. Read `AGENT_RULES.md`, `PROGRESS.md`, `TASKS.json` in full. Repo was empty of projects.
2. Generated candidates and ran prior-art searches before building.
3. **Rejected candidate 1** (a crontab linter with DST and `%`-escaping checks): GitHub
   search found materially equivalent published tools — `SNO7E-G/CronLens` ("lint cron
   expressions ... with DST, overlap and thundering-herd warnings"),
   `HeytalePazguato/cron-doctor` ("ten lint checks"), `zbcdo/cronlint`. Same problem, user,
   workflow and deployment model, so the candidate was dropped rather than reframed.
4. **Selected candidate 2: backfire** — a static analyzer that composes retry policies
   along a Python call graph and reports worst-case attempts and wall-clock time for one
   logical call. Searched GitHub, PyPI, npm, web, forums and issue trackers across 10+
   query formulations; the closest things found are single-site Semgrep rules, a retry
   simulator, an arXiv prevalence study, and service-mesh retry budgets. Novelty confidence
   recorded as **Medium** (arxiv.org is blocked by this environment's egress policy, so the
   closest academic item could not be read directly). Details in
   `projects/backfire/NOVELTY_REPORT.md`.
5. Built and validated it. 85 tests pass. Ran it on three real codebases and on itself.

## Blocker: could not create a new repository

`AGENT_RULES.md` rule 5 and the protocol's Section 0.1 require each project to live in its
own new repository. Repository creation is not available to this session:

- `mcp__github__create_repository` → `403 Resource not accessible by integration`
- `POST https://api.github.com/user/repos` with `$GH_TOKEN` → `403 This GitHub API path is
  not available: sessions are bound to their configured repositories.`

So the finished project was committed inside this control repository at
`projects/backfire/` instead, on branch `claude/eloquent-newton-p3qht6`. The directory is
self-contained (own `LICENSE.txt`, `pyproject.toml`, CI workflow) and can be moved to its
own repository unchanged. To unblock a future run: pre-create the repository and add it to
the session's allowed repositories, or grant repository-creation scope.

Note: `projects/backfire/.github/workflows/ci.yml` does not run while nested — GitHub only
reads workflows at a repository root. It becomes active once the project is moved.

## Evidence for the claims in the README

All numbers come from runs made this session on CPython 3.11.15, Linux x86_64 container:

- Tests: `pytest -q` → 85 passed.
- Install path: `pip install .` into a fresh venv, then `backfire --version` and a scan.
- `psf/requests` @ `dae7ef6` (`src`): 19 files, 245 functions, 0 retry sites, 0 findings, 0.14s.
- `openai/openai-python` @ `d7c41ef` (`src`): 1840 files, 3919 functions, 14 retry sites,
  0 findings, 1.66s.
- `PrefectHQ/prefect` @ `d82220b` (`src`): 1268 files, 12746 functions, 41 retry sites,
  29 findings (22 BF002, 6 BF003, 1 BF004), 5.46s.
- Determinism control: two consecutive prefect runs produced byte-identical JSON.
- False-positive control: requests and openai-python, which retry in a single layer, report
  no amplification.

Three precision bugs were found by running against those real codebases and fixed with
regression tests: a crash on `self()` calls, retry-loop over-detection on streaming and
fan-out loops, and "unbounded" being reported where the attempt cap was merely unreadable
(module-level constants are now resolved).

## Next action

Either move `projects/backfire/` into its own repository once creation is possible, or pick
the next project. If picking a new project, start again at the prior-art search; do not
reuse this report's scope.
