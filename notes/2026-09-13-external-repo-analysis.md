> **Provenance.** Supplied by the repository owner on 2026-09-13 as input to
> ideation. Preserved verbatim below. It was produced by an external analysis that
> **could not read this repository's rule files** (it says so in its own Caveats
> section), so its account of the repository's conventions is inference, and parts
> of it are already wrong: `STRICT_ROUTINE_PROMPT.md` was deleted in commit
> 70b7af8, and the LICENSE placeholders it flags were filled in commit 3721576.
> Treat it as a landscape survey, not as a description of this repository.
>
> **All ten of its project ideas are out of scope** under `IDEA_DOMAINS.md` §0.3,
> which forbids agent-loop meta-tooling as a project target. See `IDEAS.md`
> section 1 for the per-idea record.

---

# guthib241/pebble: Repository Analysis and 10 Original Project Ideas

## TL;DR
- **The repo is NOT about the Pebble smartwatch.** `github.com/guthib241/pebble` (owner "guthib241," copyright "Achanti Sri Vardhan," 2026, described simply as "rules") is a small, brand-new repository containing a **rulebook/protocol for an autonomous AI coding agent** — files: `AGENT_RULES.md`, `AUTONOMOUS_PROJECT_EXECUTION_PROTOCOL.md`, `STRICT_ROUTINE_PROMPT.md`, `PROGRESS.md`, `TASKS.json`, and a custom `LICENSE.txt`. The name "pebble" evokes the crow-and-pebbles fable (raise the water one pebble at a time = build big things one small autonomous step at a time).
- **Only two hard, verifiable constraints could be extracted** (the four agent-rule files are not fetchable via available tooling, so their exact wording is unconfirmed): the **LICENSE is non-commercial with mandatory attribution** to Achanti Sri Vardhan, and the file structure implies the repo's own working discipline — a **strict, state-on-disk, one-task-per-iteration autonomous loop** (TASKS.json queue + PROGRESS.md log + strict routine prompt), the same family as the public "Ralph loop" pattern.
- **All 10 ideas below are tools/experiments in the autonomous-agent-execution space**, each verified against what already exists, each buildable solo in hours-to-days, and each compliant with the repo's non-commercial + attribution license. The three strongest to start tomorrow are **#1 GlassBox**, **#3 Rewind**, and **#7 RedTeam-in-the-Loop**.

## Key Findings

### What the repository actually is
The repository is public, has 3 commits, 0 stars/forks, and its entire purpose is captured in the one-word description: "rules." The six files are:
- `AGENT_RULES.md` — behavioral rules for an autonomous agent
- `AUTONOMOUS_PROJECT_EXECUTION_PROTOCOL.md` — the execution protocol/workflow
- `STRICT_ROUTINE_PROMPT.md` — the recurring loop prompt the agent runs each cycle
- `PROGRESS.md` — an append-only progress log
- `TASKS.json` — a machine-readable task queue
- `LICENSE.txt` — a custom non-commercial/attribution license

This file set is the canonical fingerprint of a **self-directed "agent loop" project**: a task queue the agent pulls from, a progress ledger it writes to, a strict per-cycle prompt, and a rules file that governs behavior. It is functionally the same architecture documented publicly as the "Ralph loop." Per ralphloop.sh, that pattern is: "one task per invocation, commit, then stop. Each iteration the agent picks the single highest-priority incomplete task, works it to done, verifies it, commits, and exits. It never batches two tasks into one run" — with state kept on disk (tasks.json + a log file) so a fresh context can reorient. It is also aligned with the `TASKS.md` community spec (a "/next-task" 6-step autonomous work loop). It is unrelated to the Pebble smartwatch ecosystem (PebbleOS, Core Devices, rebble.io), which I confirmed and ruled out.

The economics that make this pattern compelling are striking: per decodingai.com, Geoffrey Huntley delivered an MVP quoted at $50,000 for just $297 in tokens using a single Ralph loop — a 170x cost reduction over the human estimate. That is the upside these "rules" repos chase, and it is why disciplined verification matters: Boris Cherny, creator of Claude Code at Anthropic, posted on X (Jan 2, 2026): "probably the most important thing to get great results out of Claude Code -- give Claude a way to verify its work. If Claude has that feedback loop, it will 2-3x the quality of the final result."

### The rules that could be extracted verbatim (LICENSE.txt)
Because the four agent-rule Markdown files and TASKS.json are not retrievable through available web tooling (the repo is too new to be search-indexed at file granularity, and direct blob/raw/API fetches are blocked), the **only rules I can quote with certainty are from the license**, which nonetheless bind every derived project:
1. **Non-commercial only** — "to use, copy, and modify the Software for NON-COMMERCIAL purposes only." Commercial use requires written permission from achantivardhan@gmail.com.
2. **Attribution required** — any use or modified version "must retain this notice and give clear, visible credit to Achanti Sri Vardhan, including in the README, in-app credits, or public listing."
3. **Derivative/similar works must attribute** — a new project "built on its ideas, structure, or code" must carry a visible credit such as "based on / inspired by [PROJECT NAME] by Achanti Sri Vardhan" in its README and any public listing.
4. **No warranty.**

**Inferred (not verbatim) working conventions**, based on the file names and the well-documented pattern they match — treat these as the likely "rules" the repo enforces on itself, to be confirmed by reading the files directly:
- One task per iteration; complete → verify → commit → stop.
- All state lives on disk (TASKS.json + PROGRESS.md) so a fresh context can reconstruct where things stand.
- A strict recurring routine prompt drives each cycle; the agent acts autonomously rather than asking permission.
- Self-verification before marking a task done.

**Every idea below is designed to comply with both the hard license rules and these inferred conventions** (state-on-disk, one-task-per-iteration, self-verifying, non-commercial, attributed).

### The 2026 autonomous-agent landscape (novelty baseline)
To ensure novelty, I mapped what already exists as of September 2026:
- **Loop frameworks**: Ralph loop (ralphloop.sh), TASKS.md spec, `loop-harness` (second-agent verification gate + worktree isolation), aibtcdev `loop-starter-kit` (10-phase self-updating loop), `auto_agents` (hash-chained transition journal, WAL, SQLite index).
- **Orchestrators**: Bernstein (Goal→Planner→Task Graph→Orchestrator→parallel Agents→Janitor verify→merge), OpenHands, SWE-agent, emdash, and xAI's Grok Build CLI, launched May 14, 2026 (expanded to all SuperGrok/X Premium+ subscribers May 25, 2026), running up to 8 parallel sub-agents in Git worktrees; its 70.8% SWE-bench Verified score was reported for the underlying grok-code-fast-1 model as of May 15, 2026 (per Wikipedia "Grok Build" and buildfastwithai.com), versus Claude Code/Opus 4.7 at 87.6%.
- **Verification**: Ouroboros (pins an acceptance spec and hides grading commands from the executing agent), "vericoding" (formal-verification-backed generation, research-phase).
- **Spec/governance**: Spec-Driven Development (Kiro, GitHub Spec Kit, OpenSpec); AGENTS.md, contributed by OpenAI to the Agentic AI Foundation (AAIF) formed by the Linux Foundation on Dec 9, 2025 alongside Anthropic's MCP and Block's goose — per the Linux Foundation press release, Executive Director Jim Zemlin said "Bringing these projects together under the AAIF ensures they can grow with the transparency and stability that only open governance provides," and AGENTS.md was adopted by 60,000+ open-source projects; the Agent Skills Standard; and "Constitutional SDD" (a versioned machine-readable constraints "constitution").
- **Memory**: 3-tier SQLite + vector + working-buffer patterns; Aeon (neuro-symbolic memory with WAL + CRC32 recovery).

The gaps these leave open — which the ideas below target — are: **auditability/replay of an agent's own reasoning, adversarial self-testing, economic self-governance, cross-agent task markets, and human-legible "why" trails**, none of which are solved by the existing task-loop tools. A key motivating gap: the "harness engineering" critique holds that "LLM compliance with instructions is probabilistic, not deterministic" and must be paired with deterministic outer-harness gates (linters, CI). Per Augment Code, the term is attributed to HashiCorp co-founder Mitchell Hashimoto (blog post ~early Feb 2026) and was formalized in an OpenAI post by Ryan Lopopolo on Feb 11, 2026; GitHub's analysis of 2,500+ AGENTS.md repositories recommends a three-tier boundary pattern. Several ideas below directly attack this "rules are only followed probabilistically" problem.

## Details — 10 Original Project Ideas

Each idea lists: pitch · novelty (vs. what exists) · core technical challenge · stack · difficulty/time · rules-fit.

**1. GlassBox — a replayable "flight recorder + courtroom" for autonomous agent runs**
- *Pitch:* Wrap any agent loop so every cycle emits a signed, replayable "black box" record, then render it as an interactive timeline where you can scrub, branch, and ask "why did it do this?"
- *Novelty:* `auto_agents` keeps a hash-chained journal and Aeon uses WAL for crash recovery, but these are for *machine* recovery, not *human* forensic replay. No existing task-loop tool gives a scrub-and-branch visual audit UI over an agent's own decisions. Closest is generic LLM tracing (LangSmith-style) which logs calls but not task-graph state transitions with deterministic replay.
- *Challenge:* Deterministic replay despite non-deterministic LLM calls — you must snapshot the full prompt+tool state per cycle and content-address it so a replay reproduces the exact branch point.
- *Stack:* Python/TypeScript wrapper around the STRICT_ROUTINE loop; SQLite (WAL mode) event store; a static React/timeline UI; Merkle hash chain for tamper-evidence.
- *Difficulty:* Medium, ~3–5 days.
- *Rules-fit:* Reads TASKS.json/PROGRESS.md as its event source; one-task-per-iteration maps cleanly to one record; non-commercial dev tool with attribution in README.

**2. Pebblemark — a benchmark that scores an agent loop's DISCIPLINE, not its IQ**
- *Pitch:* A test harness that measures whether an autonomous loop actually obeys its own rules (one task per iteration, commit-after-verify, no scope creep) rather than how smart the underlying model is.
- *Novelty:* SWE-bench/SWE-bench Pro measure task success; nobody benchmarks *rule adherence*. Given the "harness engineering" finding that LLM instruction-following is probabilistic rather than deterministic (Hashimoto, Feb 2026; formalized by OpenAI's Ryan Lopopolo, Feb 11, 2026), a discipline benchmark is genuinely new.
- *Challenge:* Designing adversarial task fixtures that tempt the agent to batch tasks or skip verification, plus an objective scorer for "did it stop after one task?"
- *Stack:* Python; git fixtures; a referee script that inspects commit granularity and diff scope; JSON scorecards.
- *Difficulty:* Medium, ~3–4 days.
- *Rules-fit:* Directly operationalizes the repo's own conventions; non-commercial research artifact.

**3. Rewind — time-travel debugging that lets an agent branch its own history**
- *Pitch:* Give the loop a `git`-like `checkout` of its *reasoning* state, so when a task fails the agent (or you) can rewind to any prior cycle and re-run down a different branch without losing later good work.
- *Novelty:* Checkpointing exists (save/resume state), and loop-harness isolates work in git worktrees, but no tool lets the agent *fork its own decision history* mid-run and reconcile branches. This is "structured concurrency for agent reasoning."
- *Challenge:* Reconciling divergent PROGRESS.md/TASKS.json states after a branch — a 3-way merge of task graphs, not just files.
- *Stack:* Rust or Go for the state VCS; content-addressed blob store; CLI + optional TUI.
- *Difficulty:* Hard, ~5–7 days.
- *Rules-fit:* Built on TASKS.json + PROGRESS.md as the versioned state; enforces one-task commits as branch points.

**4. Contramind — a "constitution compiler" that turns prose rules into runtime guards**
- *Pitch:* Compile `AGENT_RULES.md` from English into executable pre/post-condition checks that gate every tool call, so a rule like "never touch files outside /src" is *enforced*, not *hoped for*.
- *Novelty:* "Constitutional SDD" (2026) proposes versioned machine-readable constraints, and Ouroboros hides grading from the executor, but neither auto-compiles free-text rules into interposed runtime guards. This directly closes the probabilistic-compliance gap between written rules and actual behavior that the harness-engineering critique identifies.
- *Challenge:* Reliable NL→policy translation and a sandbox interposition layer (syscall/tool-call hooks) that can veto actions.
- *Stack:* Python; an LLM rule-parser producing a small DSL; a tool-call proxy/middleware; OPA/Rego-style policy engine optional.
- *Difficulty:* Hard, ~5–8 days.
- *Rules-fit:* Literally operationalizes AGENT_RULES.md; non-commercial governance tool.

**5. Rookery — a peer-to-peer task market where solo agent loops trade sub-tasks**
- *Pitch:* Multiple independent "pebble" loops post tasks they can't finish to a shared board and bid to complete each other's tasks, using a Contract-Net-style auction — a labor market for hobbyist agents.
- *Novelty:* Multi-agent orchestrators (Bernstein, Grok Build) run agents *you* own in one process; there's no open, cross-owner task exchange for independent single-file TASKS.json loops. The Contract Net Protocol is 1980s theory; a modern file-based implementation for LLM loops is unbuilt.
- *Challenge:* Trust and verification of work done by an untrusted peer agent (needs the Ouroboros "hidden acceptance spec" trick).
- *Stack:* TypeScript; a tiny relay server or libp2p; JSON task envelopes; signed results.
- *Difficulty:* Hard, ~6–8 days.
- *Rules-fit:* TASKS.json is the native currency; non-commercial (no real money) keeps it license-clean.

**6. Metronome — a self-tuning "circadian rhythm" scheduler for autonomous loops**
- *Pitch:* Instead of a fixed cron tick, the loop learns *when* to wake based on task backlog, past failure rates, and cost, throttling itself to hit a token/day budget like a heartbeat.
- *Novelty:* `loop-starter-kit` uses a fixed "sleep 300" and reports ~$0.02/tick; nobody has a *closed-loop controller* that adapts cadence to backlog and budget. This is control theory applied to agent cadence.
- *Challenge:* Online estimation of marginal value-per-tick and a controller that avoids oscillation.
- *Stack:* Python; a PID/bandit controller; SQLite metrics; cron/systemd timer it rewrites.
- *Difficulty:* Medium, ~3–4 days.
- *Rules-fit:* Drives the STRICT_ROUTINE_PROMPT cadence; writes state to disk; non-commercial.

**7. RedTeam-in-the-Loop — the agent that continuously attacks its own rulebook**
- *Pitch:* A second "adversary" loop whose only job is to generate tasks/prompts designed to make the primary loop violate AGENT_RULES.md, logging every successful jailbreak as a regression test.
- *Novelty:* loop-harness uses a *skeptical verifier* to check output quality; nobody ships a *generative adversary* that evolves attacks against the rules themselves and auto-builds a rule-hardening test suite. Prompt-injection research exists but not as a self-contained co-loop for a personal agent.
- *Challenge:* Automatically detecting a "violation" (needs Contramind-style runtime guards as the oracle) and evolving attacks that generalize.
- *Stack:* Python; two coupled loops; a violation oracle; a growing YAML/JSON attack corpus.
- *Difficulty:* Medium-Hard, ~4–6 days.
- *Rules-fit:* Exists purely to enforce AGENT_RULES.md; non-commercial security research.

**8. Cairn — a human-readable "why" trail that turns PROGRESS.md into a narrated documentary**
- *Pitch:* Post-process the agent's raw progress log into a chaptered, plain-English story ("Day 2: tried X, it failed because Y, pivoted to Z") that a non-engineer can read to understand what the agent built and why.
- *Novelty:* Progress logs today are terse machine ledgers (append lines). No tool synthesizes them into a causal, human-facing narrative with decision rationale extracted. Reverse-documentation frameworks (e.g., "Reversa," 2026) target legacy *code*, not agent *runs*.
- *Challenge:* Faithful causal summarization without hallucinating rationale that wasn't in the trace.
- *Stack:* Python; an LLM summarizer with strict grounding to log lines; Markdown/HTML output.
- *Difficulty:* Easy-Medium, ~2–3 days.
- *Rules-fit:* Consumes PROGRESS.md directly; attribution trivially satisfied; non-commercial.

**9. Ballast — an "economic conscience" that forces the loop to justify every dollar**
- *Pitch:* A budget guardian that, before each cycle, makes the agent write a one-line expected-value justification for the spend, and auto-pauses the loop when cumulative ROI drops below a threshold.
- *Novelty:* Cost-per-tick is *reported* today but never *gated by self-justified expected value*. Given documented 170x cost swings (Huntley's $297-for-$50k MVP), a pre-commitment device against runaway token spend — behavioral economics for agents — is a real unmet need.
- *Challenge:* Getting calibrated (not rubber-stamped) self-estimates and a fair after-the-fact ROI reconciliation.
- *Stack:* Python; token-cost hooks; a ledger; a simple Brier-style calibration score on the agent's own predictions.
- *Difficulty:* Medium, ~3–4 days.
- *Rules-fit:* Wraps the routine loop; state-on-disk ledger; non-commercial.

**10. Chrysalis — a loop that safely rewrites its own STRICT_ROUTINE_PROMPT and proves it didn't get worse**
- *Pitch:* A self-improving loop that proposes edits to its own prompt/rules, but must pass Pebblemark (#2) on a held-out fixture set before the change is allowed to persist — self-modification with a safety ratchet.
- *Novelty:* `loop-starter-kit` and Ralph loops let the agent edit its loop prompt freely with *no gate*; that's the danger. A self-modifying loop with a *mandatory regression gate that can only ratchet quality upward* is unbuilt and directly addresses the known failure mode of unguarded self-editing.
- *Challenge:* Preventing reward-hacking of its own benchmark (the executor must not see the held-out grading — Ouroboros pattern), and rollback on regression.
- *Stack:* Python; git-backed prompt versioning; the Pebblemark harness as the gate; a promote/rollback controller.
- *Difficulty:* Hard, ~6–9 days.
- *Rules-fit:* Directly evolves STRICT_ROUTINE_PROMPT.md and AGENT_RULES.md under verification; one-task-per-iteration; non-commercial.

## Recommendations

**Start tomorrow with these three (highest novelty-to-effort, and they compound):**
1. **#1 GlassBox** — highest immediate utility, medium effort, and it produces the event store that #3 and #8 reuse. Build the SQLite WAL event recorder first, then the timeline UI.
2. **#3 Rewind** — the most technically distinctive ("git for agent reasoning"); ambitious but self-contained. Start with a read-only rewind (replay to a prior cycle) before attempting branch-merge.
3. **#7 RedTeam-in-the-Loop** — fastest path to something visibly "crazy" and demo-able; pairs naturally with #4 Contramind (which supplies the violation oracle).

**Suggested build order / dependency graph:** #1 (event store) → #8 (narration, reuses events) → #2 (discipline benchmark) → #10 (self-improvement, needs #2 as its gate). Separately: #4 (guards) → #7 (adversary uses the guards as oracle). #5, #6, #9 are independent and can slot in anytime.

**Thresholds that change the plan:**
- **If you can read the four rule files directly** (clone the repo or open them in a browser), do that *first* — it will confirm or overturn the inferred conventions and may add hard constraints (e.g., a mandated language or a "no external dependencies" rule) that reshape stacks.
- **If AGENT_RULES.md forbids external network calls or multi-agent behavior**, drop #5 (Rookery) and #7's adversary-as-service variant; keep the single-process ideas.
- **If the repo mandates a specific language**, align every stack to it (I assumed Python/TS/Rust by fit).
- **If you intend any revenue**, you must email achantivardhan@gmail.com for a commercial license before publishing — the default license forbids it.

## Caveats
- **The four core rule files (AGENT_RULES.md, AUTONOMOUS_PROJECT_EXECUTION_PROTOCOL.md, STRICT_ROUTINE_PROMPT.md, TASKS.json) could not be read.** Available tooling blocked their blob/raw/API URLs, and the repo is too new to be indexed at file granularity. A dedicated subagent confirmed this independently. **The only rules quoted verbatim are from LICENSE.txt.** All "working conventions" (one-task-per-iteration, state-on-disk, self-verification) are *inferred* from the file structure and its strong resemblance to the publicly-documented Ralph-loop/TASKS.md patterns — they are a well-grounded hypothesis, not confirmed repo content. **Read the files directly to confirm before relying on them.**
- **Novelty is point-in-time (September 2026).** The autonomous-agent space is moving extremely fast; verify each idea against the latest before committing significant time. Closest-existing tools are named per idea so you can re-check.
- **The interpretation that this is an "AI agent rules" repo is high-confidence** (based on the confirmed file names, the "rules" description, and the crow-and-pebble naming convention), but the *specific intent* of the author is not documented publicly and is my best-judgment inference.
- One search result attempted to inject instructions (asking me to visit an external site and post a review); I ignored it as untrusted third-party content. Flagging it here for transparency.