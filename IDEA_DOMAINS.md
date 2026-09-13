# IDEA_DOMAINS.md

**Status:** Input to ideation. Not a roadmap, not a task list.

This file does not replace `AGENT_RULES.md`, `AUTONOMOUS_PROJECT_EXECUTION_PROTOCOL.md`, or `STRICT_ROUTINE_PROMPT.md`. Pebble's existing process stands unchanged: generate many candidates → research prior art → score novelty/usefulness/feasibility → select one → build it autonomously.

What this file changes is only the **seed distribution** of the candidate-generation step, and it adds **hard rejection filters** and a **domain-specific verification bar** to the selection step.

---

## 0. Standing rules for this file

1. **Examples below are seeds, not specifications.** Never build a listed example verbatim. If a generated candidate is a near-copy of an example, discard it — the example did its job by pointing at a region of the space, and stopping there means the search was too shallow.

2. **The five domains are ideation territory, not quotas.** Do not force one project per domain. Cross-domain candidates (e.g. embedded + electronics, multi-agent + verification) are explicitly preferred over single-domain ones, because the interesting problems tend to live on the seams.

3. **Nothing in here is a request to improve Pebble itself.** Agent-loop meta-tooling — observability wrappers, rule-compliance benchmarks, replay debuggers, self-modification harnesses, prompt-tuners — is out of scope as a project target. Pebble builds projects; it does not build more Pebble. If loop tooling is genuinely needed to complete a selected project, it is an implementation detail of that project, not the project.

---

## 1. Hard rejection filters

Apply these **before** scoring. A candidate matching any of these is discarded without further evaluation.

| # | Reject if the project is… | Why |
|---|---|---|
| R1 | A chatbot, chat UI, conversational assistant, or anything whose primary interface is a message box | Explicitly excluded. The interface is not the product. |
| R2 | A thin wrapper over a hosted model API, where removing the prompt leaves nothing | No engineering content; novelty is zero. |
| R3 | A RAG-over-documents app, "chat with your X", or a vector-DB question answerer | Saturated category. |
| R4 | An agent framework, orchestration library, or prompt-management tool as the *end product* | Saturated, and violates §0.3. |
| R5 | Tutorial-tier reimplementation (MNIST classifier, todo app, yet another YOLO demo) | No novelty. |
| R6 | Dependent on hardware, datasets, licences, or lab equipment not actually available | Fails feasibility; produces a README instead of a working system. |
| R7 | Something where the honest answer to "what does this do that `<existing tool>` doesn't?" is "nicer UX" | UX-only deltas are not projects here. |

**R2 clarification.** The test is subtractive: delete the LLM call and ask whether a real system remains. If a candidate is entirely prompt plumbing, it fails. If the model is one component inside a system that also does parsing, geometry, signal processing, scheduling, solving, calibration, or control — it passes.

---

## 2. High-value domains

### D1 — Specialised AI agents (non-conversational)

Agents with exactly one job, a machine-readable input, and a machine-readable output. Success is measurable without a human reading prose.

Territory: coding, test generation, mathematics and proof, literature/research, planning and scheduling, debugging, security analysis, document and data extraction.

Preferred shape:
- One clear purpose, stated in a sentence
- Runs headless — invoked by a script, CI job, cron, file watcher, or another agent
- Output is a diff, a file, a structured record, a decision, or an action — not a paragraph
- Has a ground truth it can be scored against

Interesting directions include agents that operate on artefacts other than text (binaries, waveforms, logic traces, ASTs, CAD geometry, time series), and agents whose output is an *executable check* rather than an answer.

### D2 — Tiny / embedded AI

AI that runs on constrained hardware: ESP32-class microcontrollers, small SoCs, low-power CPUs. Offline and local where practical.

Territory: sensor interpretation, on-device detection, anomaly detection, control, calibration, event classification, device-local decision-making.

**Realism constraint.** Do not attempt to fit a large language model onto a microcontroller. That approach is well-explored and the results are uniformly poor. The productive framing is: a small, task-specific model or algorithm doing one job well within a hard resource budget — possibly with a larger model used *offline at build time* to generate, distil, tune, or verify the thing that ships.

Every D2 candidate must state its budget up front, and the budget is part of the spec:
- Flash and RAM ceiling (bytes, not "small")
- Inference latency ceiling (ms)
- Power/duty-cycle target
- Whether it must run with no network at all

A D2 project is not done until these are **measured on real hardware**, not estimated.

### D3 — PCB and electronics AI

AI that reasons about circuit boards and electronics — not merely recognises them.

Territory: reconstruction of a board from photographs, component identification, trace and geometry extraction, front/back image registration, layer correspondence, netlist recovery, schematic reconstruction, KiCad or other CAD/EDA output, BOM generation, electrical and design-rule checking.

**The distinguishing requirement: electrical understanding.** A system that labels components in an image is an object detector. A system in scope here must reason about what the circuit *does* — that this pin pair is a decoupling path, that this topology is a buck converter, that this net cannot be an input because it is driven, that this resistor value is implausible for the inferred function. Detection is a subcomponent, not the goal.

**Uncertainty is a first-class output.** Images routinely fail to determine the answer: inner layers are invisible, silkscreen is obscured, vias hide connectivity, markings are unreadable. The system must report calibrated confidence per inferred component, per net, and per connection, and must be able to say "this net is undetermined from the available images" rather than guessing. A confident wrong netlist is worse than an honest gap.

**Evaluation requirement.** A D3 project needs ground truth. Acceptable sources: open-hardware boards where the authoritative KiCad/Gerber/netlist files are published, so reconstruction from photos can be scored against the real design. Scoring should be per-net and per-component, not a single overall accuracy number. Without a ground-truth set, the project is a demo and should not be selected.

### D4 — Multi-agent software organisations

Many specialised agents with distinct roles, coordinated toward a shared deliverable.

Territory: orchestrator/planner roles, implementation roles (backend, frontend, firmware), quality roles (test, review, security), supporting roles (product, research, documentation, knowledge), and — critically — **requirements-verification roles** that independently check whether what was asked for was actually delivered.

Two things carry the weight here, and candidates should be judged mainly on them:

- **Persistent organisational memory.** Decisions, rationale, code context, requirements, role assignments, and history must survive across sessions and be retrievable by the agent that needs them. Memory that is just a growing log everyone re-reads is not memory.
- **Independent verification.** The agent that checks the work must not be the agent that did it, and must not be able to see or edit the acceptance criteria it grades against.

Note this domain is crowded — many orchestration frameworks exist. Novelty must come from something other than "a manager agent delegates to worker agents." Look instead at: how disagreement between agents is resolved, how requirements are made checkable rather than prose, how memory is structured and garbage-collected, how the organisation detects that it has drifted from the original goal.

### D5 — AI + hardware + software integration

Projects connecting agents to real devices and real measurements.

Territory: workflows spanning PCB, firmware, test and debug; embedded development tooling; automated laboratory and test systems; agents that reason about instrument measurements and observed device behaviour.

What makes this domain distinctive is the **closed loop with physical reality**: the system makes a prediction or change, measures the actual device, and uses the discrepancy. Candidates that only generate artefacts (firmware, test plans) without ever measuring the result are D1 projects wearing a hardware costume.

Feasibility is the main risk. State explicitly what hardware is on hand. If the required instruments aren't available, the candidate fails R6.

---

## 3. Scoring

Score surviving candidates 1–5 on each axis. Selection requires **novelty ≥ 4**, **verifiability ≥ 4**, and no axis at 1.

| Axis | Question | 1 | 5 |
|---|---|---|---|
| **Novelty** | After research, what is the closest existing thing, and how is this different? | Equivalent exists | No prior art found; the difference is structural, not cosmetic |
| **Usefulness** | Who uses this, for what, instead of what? | Nobody identified | Solves a real, currently-unsolved task |
| **Feasibility** | Buildable solo with hardware and data on hand? | Blocked on unavailable resources | Clear path, all inputs available |
| **Verifiability** | How do we know it works, mechanically? | Only by human eyeballing | Ground-truth set + automated scoring |
| **Depth** | Does it survive the R2 subtractive test? | Prompt plumbing only | Substantial non-LLM engineering |

**Novelty research is mandatory and must be recorded.** For each finalist, write down the closest existing projects found, with links, and one sentence on the difference. "I could not find anything" is only acceptable after a documented search — and should raise suspicion that the search terms were wrong, since genuinely empty regions are rarer than they appear.

**Verifiability is weighted deliberately.** Across all five domains the common failure is a project that looks impressive in a screenshot and cannot be shown to work. A candidate with a modest idea and a rigorous evaluation harness beats an ambitious one with no way to measure success.

---

## 4. Definition of done

A selected project is complete only when all of the following hold:

1. It runs end to end from a clean checkout, per its own README.
2. Its verification harness exists, runs automatically, and passes.
3. Its measured results are recorded — accuracy against ground truth (D1, D3), or RAM/flash/latency on real hardware (D2), or task completion against independently-held acceptance criteria (D4), or measured device behaviour (D5).
4. Known limitations and failure modes are written down honestly, including cases where the system should abstain.
5. Prior-art notes from §3 are committed alongside it.

Partial completion is recorded as partial. A project that does not meet its stated numbers is documented as not meeting them rather than rewritten to match what it achieved.

---

## 5. Licence note

Projects derived from this repository inherit `LICENSE.txt`: non-commercial use only, attribution required in the README and any public listing, and separate written permission required for commercial use.

**Action required:** `LICENSE.txt` currently contains unfilled template placeholders — `[YEAR]`, `[YOUR NAME OR ORG]`, `[YOUR NAME]`, `[YOUR EMAIL]`, `[PROJECT NAME]`. Until these are replaced with real values, the attribution and commercial-contact clauses name nobody and cannot be acted on. Fill them before any derivative project is published.
