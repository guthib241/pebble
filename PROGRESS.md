# Progress

Status: in progress
Current project: `orbiter` (folder `orbiter/`)

## What orbiter is

Flags Python code that mixes units, like milliseconds passed as seconds. Static
analyzer over the `ast` module, standard library only.

## Run log

### 2026-09-12 (run 1)

- Intake: read `AGENT_RULES.md`, `PROGRESS.md`, `TASKS.json`. `current_project` was
  null and the repository contained no project folders, so a new project was selected.
- Prior-art search performed across GitHub repository pages, PyPI, the flake8 plugin
  index, academic sources, tool documentation, and forum/Q&A results. Full record in
  `orbiter/NOVELTY_REPORT.md`.
- Candidate 1 (cron DST hazard auditor) rejected: `cronkit` and several DST-aware cron
  checkers cover the capability materially.
- Candidate 2 (Python swapped-argument detector) set aside: the capability exists as a
  research artefact for Python (DeepBugs IntelliJ plugin, eth-sri argument-swap task).
- Candidate 3 (`orbiter`) selected. Novelty confidence Medium. Closest prior art:
  Phys / Phriky-Units, which do the same kind of annotation-free unit inconsistency
  detection for ROS C++; no Python equivalent was found.
- `NOVELTY_REPORT.md` written before implementation, as required.

Next action: implement the analyzer modules, then tests, then README.
