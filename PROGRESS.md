# Progress

Status: `orbiter` is complete and pushed. No project in progress.
Current project: none (see `TASKS.json`)

## Completed projects

### orbiter (folder `orbiter/`)

Flags Python code that mixes units, like milliseconds passed as seconds. A static
analyzer over the `ast` module, standard library only, Python 3.11 or newer.

It infers a unit and a numeric scale for expressions from identifier names,
`typing.Annotated` metadata, and a table of standard-library call conventions, then
reports mismatches in call arguments (ORB001), arithmetic and comparisons (ORB002),
assignments (ORB003) and return values (ORB004). Constant factors are read as
conversions when they land on a real unit, so `time.sleep(timeout_ms / 1000)` is
accepted while `time.sleep(timeout_ms)` is reported.

State: finished. 151 tests pass. README, novelty report, license and reproducible
evidence are all in the folder.

## Run log

### 2026-09-12 (run 1)

Intake: read `AGENT_RULES.md`, `PROGRESS.md`, `TASKS.json`. `current_project` was null
and the repository held no project folders, so a new project was selected.

Prior-art search across GitHub repository pages, PyPI, the flake8 plugin index,
academic sources (arXiv, ACM DL, ScienceDirect, Semantic Scholar), tool documentation
and forum results. Full record in `orbiter/NOVELTY_REPORT.md`.

- Candidate 1, a cron DST hazard auditor: **rejected**. `cronkit` provides CLI crontab
  linting with overlap detection and schedule projection, and several DST-focused cron
  timezone checkers exist, so the capability overlapped materially.
- Candidate 2, a Python swapped-argument detector: **set aside**. The capability
  already exists for Python as a research artefact (the DeepBugs IntelliJ plugin covers
  incorrect function arguments in Python; `eth-sri/learning-real-bug-detector` has an
  argument-swap task), which would have capped novelty confidence lower.
- Candidate 3, `orbiter`: **selected**, novelty confidence Medium. Closest prior art is
  Phys / Phriky-Units, which do annotation-free unit inconsistency detection for ROS
  C++; no Python equivalent was found, and the Python options found require either
  runtime unit objects or fully declared distinct types.

Built in this order: novelty report, unit model and lexicon, standard-library
knowledge table, inference engine and checks, CLI, 151 tests, fixture project,
seeded-bug benchmark with control checks, README.

Findings worth carrying forward:

- The first corpus run over `/usr/lib/python3.11` produced 9 findings, **all false
  positives**, from two lexicon problems: `mm` (millimetre or minute) and the singular
  calendar words `second`, `minute`, `hour`, `day`, `week`, which in real code name an
  index rather than a duration. Those entries were removed, singular `bit` with them,
  and the reasoning is recorded in `orbiter/units.py`. Re-running the same corpus gave
  0 findings. Regression tests pin the exclusions.
- Removing singular `second` broke conversion constants such as `MS_PER_SECOND`, so
  names containing a `per` token are now handled separately: upper-case ones resolve to
  a numeric factor from the lexicon, lower-case ones (rates like `bytes_per_second`)
  are treated as unknown.
- Two limitations are documented rather than hidden: rates (one dimension divided by
  another) are outside the model, and a scale conclusion is suppressed whenever an
  unknown multiplier is involved. Both are marked in the benchmark as
  `# known-miss:` lines and asserted by a test, so they cannot quietly change.

Next action: `TASKS.json` has `current_project: null`, so the next run performs idea
generation and a fresh prior-art search under Section 4 of the execution protocol. The
search must treat `orbiter/` as prior art for any new candidate.
