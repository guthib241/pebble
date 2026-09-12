# Novelty Report — orbiter

**Project:** `orbiter`

**One-sentence description:** Flags Python code that mixes units, like milliseconds passed as seconds.

**Date of search:** 2026-09-12

**Searcher:** autonomous agent run (see `PROGRESS.md` in the repository root for the run record)

---

## 1. Candidate under assessment

A dependency-free Python static analyzer that infers a unit and a numeric scale for
expressions from identifier names (`timeout_ms`, `size_bytes`, `angle_deg`), from
`typing.Annotated` metadata, and from a built-in table of standard-library call
conventions (for example `time.sleep` takes seconds, `math.sin` takes radians), then
reports call arguments, arithmetic, assignments, and return values whose units are
inconsistent. Scale-aware arithmetic means a correct explicit conversion
(`time.sleep(timeout_ms / 1000)`) is accepted while the unconverted form is reported.

## 2. Search scope

In scope: static analysis tools and linters that detect unit, dimension, or
scale inconsistencies in source code; Python linter plugin ecosystems; runtime
unit libraries; academic work on unit inference and name-based bug detection.

Out of scope: runtime instrumentation systems for scientific computing not aimed at
finding inconsistencies, language-level unit type systems in languages other than the
ones named below, and commercial static analyzers whose rule lists are not public.

## 3. Sources searched

| Category | Sources actually consulted |
| --- | --- |
| Public source repositories | github.com (via web search; repository pages for `unl-nimbus-lab/phriky-units`, `unl-nimbus-lab/phys`, `GrammaTech/swap-detector`, `michaelpradel/DeepBugs`, `eth-sri/learning-real-bug-detector`) |
| Package registries | pypi.org (via web search, including a `site:pypi.org` query) |
| Plugin ecosystem indexes | `DmytroLitvinov/awesome-flake8-extensions` README (fetched and inspected in full), `flakes.orsinium.dev` listing surfaced in results |
| Academic literature | arXiv, ACM DL, ScienceDirect, Semantic Scholar, ResearchGate result pages for Phriky-Units (ISSTA/IROS 2017), Phys (FSE 2018), PhysFrame (FSE 2021), SA4U (arXiv 2210.09136), SwapD (SCAM 2020, arXiv 2009.09117), DeepBugs (OOPSLA 2018) |
| Tool documentation | clang-tidy check documentation (`bugprone-easily-swappable-parameters`, `bugprone-swapped-arguments`, `readability-suspicious-call-argument`), pylint standard checker list, flake8 documentation |
| Forums and Q&A | web search across Reddit/Stack Overflow/DEV/Medium results for unit-mixup detection and Python static analysis tooling |

## 4. Query formulations used

Recorded verbatim as issued:

1. `python linter detect unit mismatch variable names milliseconds seconds bytes static analysis identifier units inconsistency`
2. `"unit inconsistency" detection source code static analysis Phriky-Units Phys dimensional analysis identifier names research`
3. `github flake8 plugin OR pypi package units checker time seconds vs milliseconds bug "timeout" naming convention lint`
4. `site:pypi.org units dimensional analysis linter checker code "physical units" static OR annotation python package`
5. `reddit OR stackoverflow tool to catch milliseconds seconds mixup bugs python codebase naming suffix _ms convention detect automatically`
6. `research paper infer physical units from identifier names variable naming "unit" inference lexicon static analysis unit type error detection python`
7. `Phys unit inference variable names ROS C++ PhysFrame github unl-nimbus-lab tool physical unit inconsistency successor`

Queries 8–11 below were issued while assessing two earlier candidates that were
rejected (see Section 8), and also surfaced prior art relevant to this candidate:

8. `python static analysis detect swapped function arguments parameter name mismatch tool`
9. `pylint flake8 plugin check argument order swapped parameter names "swapped arguments" python linter`
10. `pypi package detect swapped arguments call site python AST checker "argument" swap bug finder github`
11. `ruff rule swapped arguments call site parameter name heuristic OR DeepBugs swapped argument detection javascript`

Pages fetched and read directly: `github.com/unl-nimbus-lab/phriky-units`,
`github.com/GrammaTech/swap-detector`, `ar5iv.labs.arxiv.org/html/2009.09117`,
`awesome-flake8-extensions` README.

## 5. Closest prior art found

**1. Phriky-Units** — <https://github.com/unl-nimbus-lab/phriky-units>
Annotation-free physical unit inconsistency detection for C++, specialised to ROS.
Open source, built on cppcheck. Superseded by Phys. Detects inconsistencies such as
adding meters to seconds. Does not analyse Python.

**2. Phys / PhysFrame** — <https://github.com/unl-nimbus-lab/phys>, <https://arxiv.org/html/2106.11266v1>
Phys performs probabilistic physical-unit assignment and inconsistency detection for
ROS C++, using variable names among its signals; PhysFrame extends the idea to frames
of reference. Both are implemented in Python but analyse C/C++ source through a
cppcheck XML dump. This is the closest prior art on mechanism: name-derived unit
inference plus inconsistency checking.

**3. SA4U** — <https://arxiv.org/pdf/2210.09136>
Static analysis for unit type errors, inferring unit types from message definitions in
UAV autopilot code (C/C++ domain). Domain-specific inference source rather than
identifier names.

**4. pint, numericalunits, astropy.units** — PyPI
Python runtime unit libraries. They catch dimensional errors only for values the
developer has explicitly wrapped in unit objects, and require rewriting the code under
analysis.

**5. mypy / `NewType` / `domain-types-linter`** — PyPI
Type-level enforcement that requires the developer to declare and annotate distinct
types everywhere. No unit vocabulary, no scale arithmetic, no inference from names.

**6. SwapD and clang-tidy argument checks** — <https://arxiv.org/pdf/2009.09117>, clang-tidy docs
Name-based call-site defect detection for C/C++, but for a different defect class
(swapped arguments, easily swappable parameters).

Searches of the flake8 plugin index, PyPI, and pylint's checker list surfaced no
Python linter that infers units from identifier names or checks unit consistency.

## 6. Feature-level comparison

| Dimension | orbiter (proposed) | Phys / Phriky-Units (closest) | pint / numericalunits | mypy + NewType |
| --- | --- | --- | --- | --- |
| Problem | Unit and scale mixups in Python code | Physical unit inconsistencies in ROS C++ | Dimensional errors in wrapped numeric values | Type confusion between declared domain types |
| Language analysed | Python | C/C++ | Python (runtime values) | Python |
| User | Python developer or CI pipeline | ROS/robotics C++ developer | Scientific Python developer | Python developer with full annotations |
| Inputs | Python source files, unmodified | C++ source plus cppcheck dump | Code rewritten to use unit objects | Code annotated with distinct types |
| Core mechanism | Identifier-name token lexicon, `Annotated` metadata, standard-library call table, scale-aware expression algebra | Unit assignment from ROS library types and names, dataflow over cppcheck AST | Runtime dimension algebra on wrapped quantities | Static type identity checking |
| Unit vocabulary | Software-engineering units: time, data size, angle, ratio/percent, frequency, length, single-currency money | SI physical units for robotics | Full SI plus user-defined | None; user-defined type names |
| Conversion awareness | Yes; `x_ms / 1000` resolves to seconds, correct conversions are not reported | Unit algebra over expressions | Yes, by construction | No |
| Workflow | `python -m orbiter src/` in a shell or CI, exit code plus text or JSON | Command-line run over a ROS package with cppcheck installed | Import library, wrap values, run program | Run mypy over annotated code |
| Outputs | Diagnostics with file, line, column, code, expected and found units | Inconsistency reports | Runtime exceptions | Type errors |
| Deployment | Standard-library-only CLI, no install required | Requires cppcheck; research tooling | Library dependency | Type checker |
| Distinguishing capability | Unit checking of unmodified, unannotated Python via name plus standard-library conventions, with scale-aware conversion recognition | Same idea for ROS C++ | Requires code change | Requires annotation of every value |

## 7. Material equivalence assessment

The core idea of inferring units without annotations and reporting inconsistencies is
established prior art, demonstrated for C++/ROS by Phriky-Units and Phys. `orbiter`
applies that idea to a different ecosystem and a different unit vocabulary, and adds
scale-aware conversion recognition against a table of Python standard-library call
conventions.

No tool was found that provides this capability for Python source code. The Python
options found either require the developer to rewrite values into unit objects (pint,
numericalunits, astropy.units) or to annotate distinct types everywhere (mypy with
`NewType`, `domain-types-linter`), so a Python developer cannot obtain `orbiter`'s
capability from the prior art found without modifying the code under analysis. The
candidate therefore passes the material equivalence test, while explicitly not
claiming that the underlying technique is new.

## 8. Candidates rejected before this one

* **Cron DST hazard auditor** (detect cron jobs that are skipped or run twice across
  daylight-saving transitions). Rejected: `cronkit` provides CLI crontab linting with
  overlap detection and schedule projection, and several DST-focused cron timezone
  checkers already exist, so the capability overlapped materially.
  Queries: `cron DST daylight saving time hazard detector tool jobs skipped or run twice crontab audit`,
  `github crontab linter simulate next runs timezone DST overlap detection CLI`.
* **Python swapped-argument detector.** Not rejected on material equivalence with a
  shipped Python tool, but set aside in favour of this candidate because the
  capability already exists for Python as a research artefact (the DeepBugs IntelliJ
  plugin covers incorrect function arguments in Python, and `eth-sri/learning-real-bug-detector`
  includes an `argument-swap` task), which would have capped novelty confidence lower.

## 9. Unresolved uncertainty

* GitHub code search and full-text PyPI search were not available in this environment;
  repository and package discovery relied on web search results, so a small or
  unindexed Python project with similar behaviour could exist without appearing here.
* SA4U's supported languages were described inconsistently across the result pages
  consulted; the paper PDF itself was not read in full, so its Python coverage (if
  any) is not established here.
* Commercial analyzers (Coverity, CodeSonar, SonarQube commercial rules) may contain
  unit-related checks that are not publicly documented.
* Whether identifier-name conventions in typical Python codebases are dense enough for
  the checker to find real defects at scale is measured here only on the corpora
  documented in `README.md`; it is not established in general.

## 10. Novelty confidence

**Medium.**

Multiple source categories were searched with multiple query formulations, the closest
matches were inspected directly, and no materially equivalent Python tool was found.
The rating is not High because the underlying technique is established prior art in an
adjacent ecosystem, and because two search channels that would most directly refute
the finding (GitHub code search, full-text package search) were unavailable.

## 11. Scope statement

This conclusion is limited to the sources and queries documented above. It is a
search-based finding, not a guarantee: it states that no materially equivalent prior
art was found within the documented search scope, and makes no claim that none exists.
