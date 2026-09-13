# Ideas

Every idea ever considered in this repository, kept permanently.

Nothing is deleted from this file. An idea that was rejected stays recorded with
the reason, so no future run spends usage rediscovering it, re-searching it, or
re-arguing it. Three runs have already lost time to this: two of them
independently generated the same cron-linter idea and independently searched and
rejected it, because neither could see the other's work.

**Read this file during Phase 1 intake, before generating any candidate.** It is
part of the repository's memory, not an appendix.

Every project referenced below exists on `main` under `projects/`, so a candidate can
be compared against the real code rather than against a description of it.

## How to use it

* Every candidate that gets as far as being considered goes in, whatever happens
  to it. No idea is too dead to record.
* File it under exactly one heading, by outcome.
* Include the date, the hook sentence attempt (even a failed one), what was
  searched, and the specific reason for the outcome. Links to prior art are
  required in section 2.
* Include a behaviour descriptor — `{interaction model, data source, medium,
  domain}` — so repeated cells are visible. All three existing projects share one:
  reads source files, prints text, developer tooling, local CLI.
* For finalists, include the 1-5 scores (hook, reach, demo-ability, originality,
  difficulty-worth-it, monetizability) and the pairwise comparison result.
* An idea may be **moved** between sections when something real changes — a hook
  is found, prior art turns out to be weaker than it looked, the environment gains
  a capability. Moving it means editing its entry and noting what changed and
  when. It does not mean deleting the history.
* Never move an idea upward to justify building it. If the reason for the move is
  "I want to build this," that is not a reason.

---

## 0. The owner's ideas — read first, every run

Ideas from the repository owner. They are not exempt from any gate: prior art,
problem value, feasibility and the hook all apply exactly as they do to your own
candidates. But they are considered **first**, and if you pass on one you record why
here, in a sentence, so the owner can see your reasoning and push back.

Treat a half-formed entry as a seed, not a specification. "Green screen but for X",
a dataset someone noticed, a stray observation — the value is the direction. Your
job is to find the buildable, surprising version of it.

Owner: add anything here, any time, in any state. One line is enough.

### Pebble Evolve — an evolutionary loop that breeds projects instead of picking one
Added 2026-09-13, from an external analysis of this repository.

The proposal: stop selecting one project per run. Instead keep a population, mutate
it, score each child on correctness plus distance from everything already built plus
a personal taste signal, and keep the surprising winners in an archive organised by
behaviour descriptor — so the system covers the space of possible projects rather
than converging on one. Related real work, all verified to exist: AlphaEvolve
(DeepMind, 2025), FunSearch, OpenEvolve, and ShinkaEvolve (Sakana AI,
arXiv:2509.19349, Apache-2.0, reports a state-of-the-art circle packing result from
150 samples using parent sampling, code-novelty rejection sampling and bandit-based
model-ensemble selection). Quality-diversity background: MAP-Elites and novelty
search. Interestingness-as-filter background: OMNI and OMNI-EPIC.

**Status: not yet evaluated.** It has not been through the gates and must not be
started as though it had. Specific things to resolve first:

* **Prior art is crowded.** Evolutionary LLM code search is an active, published,
  open-source field. Anything resembling "an evolutionary loop over programs" fails
  the material equivalence test on its own. The parts that looked unclaimed in the
  original analysis are (a) applying this at the level of whole user-facing
  projects rather than single algorithms or functions, and (b) a taste signal
  personal to one owner rather than a generic interestingness model. Those two are
  the claim to test, and they must be searched properly, not assumed.
* **The taste model needs data that does not exist yet.** It requires a body of the
  owner's own delight ratings. There are none. Until there are, that component
  cannot be built and must not be described as though it could.
* **Novelty scores are gameable.** The original proposal included a numeric novelty
  threshold. Do not adopt that: a fabricated score violates Section 19, and
  superficially-different-but-trivial output scores well on exactly this kind of
  metric. The generation mechanics already in `AGENT_RULES.md` take the useful parts
  — tail sampling, first-idea rejection, behaviour descriptors, pairwise comparison,
  red-teaming — without inventing a number.
* **Scope.** Implemented in full this is a product, not a project in this
  repository's sense. A bounded first milestone would be a vertical slice: one
  archive, one descriptor scheme, real candidates, and a visible result — not the
  whole engine.

Also from that analysis and already adopted into the rules, so not pending:
verbalized sampling / tail sampling, rejecting your own first idea, constraint
injection, cross-domain transfer, behaviour descriptors, and the red-team pass.

### IDEA_DOMAINS.md — the owner's ideation directive
Added 2026-09-13. Now committed at the repository root; read it with the other
control files. It does not replace `AGENT_RULES.md` or the execution protocol. It
changes the **seed distribution** (five domains, D1-D5), adds **seven hard
rejection filters** (R1-R7) applied *before* scoring, and sets a **verification
bar** (novelty >= 4 and verifiability >= 4, no axis at 1).

Three consequences that bind every run from now on:

1. **Section 0.3 forbids agent-loop meta-tooling as a project target.** "Pebble
   builds projects; it does not build more Pebble." Observability wrappers,
   rule-compliance benchmarks, replay debuggers, self-modification harnesses and
   prompt-tuners are out of scope as *projects*, though they are allowed as an
   implementation detail of a project that needs one.
2. **R6 removes D2 and D5 from this environment.** D2 (tiny/embedded AI) is not
   done until flash, RAM and latency are "measured on real hardware, not
   estimated"; D5 requires instruments and "state explicitly what hardware is on
   hand". This container has no microcontroller and no instruments. Both domains
   therefore fail R6 here for now. This is an environment limit, not a judgement
   on the domains: if hardware ever becomes reachable, they reopen.
3. **The live territory is D1, D3 and D4** — and D4 is largely closed by R4
   (agent framework or orchestration library as the *end product*) combined with
   0.3. So the real room is **D1 (single-purpose non-conversational agents over
   non-text artefacts) and D3 (electronics with genuine electrical
   understanding)**, which is where this run's search concentrated.

**Owner, two things to know.** First, your two documents disagree: every one of
the ten ideas in `notes/2026-09-13-external-repo-analysis.md` is agent-loop
meta-tooling, which 0.3 forbids. IDEA_DOMAINS.md is the structural directive and
wins, so all ten are recorded as rejected in section 1 below. Say so if that
reading is wrong and you wanted those built. Second, IDEA_DOMAINS.md section 5's
"Action required" on `LICENSE.txt` is **already done** and can be struck: `[YEAR]`,
`[YOUR NAME OR ORG]`, `[YOUR NAME]` and `[YOUR EMAIL]` were all filled in commit
3721576. The one remaining `[PROJECT NAME]` is not an unfilled blank -- it sits
inside the example attribution string in clause 3, which a derivative project
fills in with its own name. Nothing is blocked.

### (add yours below)

---

## 1. Rejected — failed the rules

Ideas that failed a gate for reasons other than prior art: not feasible here, no
definition of done, no first step, no real problem, inside the shape ban, or
memorable but useless.

Format: **name** — date. Hook attempt. Which gate failed and exactly why.

### C1-C10 — the ten ideas in the external repository analysis (2026-09-13)
GlassBox (replayable flight recorder for agent runs), Pebblemark (a benchmark
scoring an agent loop's rule-discipline), Rewind (time-travel debugging that
branches an agent's reasoning history), Contramind (compiling AGENT_RULES.md prose
into runtime guards), Rookery (peer-to-peer task market between agent loops),
Metronome (self-tuning cadence controller for a loop), RedTeam-in-the-Loop (an
adversary loop attacking its own rulebook), Cairn (narrating PROGRESS.md into a
readable documentary), Ballast (an expected-value gate on token spend), Chrysalis
(a loop that rewrites its own prompt behind a regression gate).

**All ten rejected on the same ground: `IDEA_DOMAINS.md` section 0.3.** Every one of
them is agent-loop meta-tooling whose subject is this repository's own execution
loop, and 0.3 puts that out of scope as a project target -- "Pebble builds
projects; it does not build more Pebble." No prior-art search was run on them,
because 0.3 is applied before scoring and prior art would not change the outcome.

Several are decent ideas and the analysis behind them is competent; the objection
is scope, not quality. Two independent notes for whoever revisits them: the
document's own Caveats section admits it **could not read this repository's rule
files**, so its account of the conventions is inference, and two specifics are
already stale -- `STRICT_ROUTINE_PROMPT.md`, which C10 proposes to evolve, was
deleted in commit 70b7af8, and the LICENSE placeholders it flags were filled in
commit 3721576. Kept verbatim at `notes/2026-09-13-external-repo-analysis.md` for
its landscape survey of the 2026 agent-loop field, which is the genuinely useful
part.
Descriptor: {wraps the agent loop, reads run state, text or timeline UI, agent
meta-tooling} -- one cell, ten times.

### P18, P19 — multi-agent organisation candidates (2026-09-13)
P18: requirements-as-executable-contracts with a verifier that cannot see the
criteria it grades against. P19: structured organisational memory with retrieval
and garbage collection, rather than a growing log everyone re-reads.
Hook attempt (P18): "The agent that grades the work is not allowed to see the
answer key."
**Rejected on R4 plus section 0.3**: both are agent frameworks or orchestration
infrastructure as the end product, which R4 forbids, and both are loop
meta-tooling under 0.3. `IDEA_DOMAINS.md` D4 itself flags the domain as crowded.
Recorded rather than dropped because the *blind-verifier* mechanic in P18 is a
good primitive and could return as a component inside a non-meta project.
Descriptor: {agents coordinating, task and memory state, structured records,
agent meta-tooling}.

### P20, P21, P22 — the hardware candidates (2026-09-13)
P20: a task-specific anomaly detector living inside a hard flash/RAM/latency
budget on a microcontroller. P21: a closed-loop agent that changes a device,
measures the real result on an instrument, and uses the discrepancy. P22: the
"no screen at all" constraint applied to board diagnosis -- a board that reports
its own state through a single LED.
**All three rejected on R6, and on Gate B feasibility.** `IDEA_DOMAINS.md` D2 is
explicit that the budget numbers must be "measured on real hardware, not
estimated", and D5 that unavailable instruments fail R6. This container has
neither a microcontroller nor an instrument. Simulating the measurement and
reporting it as a result would violate Section 19 outright.
**These reopen the moment hardware is reachable** -- they are blocked by the
environment, not by the idea. If the owner has a board and a logic analyser on a
desk, say so and D2/D5 become the most interesting territory in the file.
Descriptor: {runs on device, sensor signal, physical behaviour, embedded}.

### P11 — "an agent whose output is an executable check rather than an answer"
2026-09-13. **Rejected on Gate D**: as stated it is a shape, not a project. No
definition of done, no first input, no way to tell whether it has been reached.
Kept because the *shape* is a good one and `IDEA_DOMAINS.md` D1 names it
explicitly; a concrete instance of it (see P9, P10) can still qualify.

### P13 — sonification of a netlist
2026-09-13. Hook attempt: "Plays you the sound of a circuit board."
**Rejected on Gate A.** Memorable, genuinely strange, and passes the shape ban --
and provides no concrete capability whatsoever. Nobody learns anything about the
board from hearing it. `AGENT_RULES.md` is explicit that memorable-and-useless
still fails Gate A. Recorded because the constraint-injection exercise that
produced it ("sound only") is worth repeating, not because this survives.
Descriptor: {listen, netlist, audio, electronics}.

### P24 — bus-contention prover over a recovered netlist
2026-09-13. Hook attempt: "Proves which two chips on this board are fighting over
the same wire."
**Rejected on the shape ban.** The output is warnings about an input file and the
success condition is a clean report. That is precisely the skeleton the ban is in
force against, and renaming the input from source code to a netlist does not
change the shape. The underlying electrical reasoning may survive inside another
candidate, as long as the deliverable is a reconstructed artifact rather than a
list of complaints.
Descriptor: {reads a file, netlist, printed findings, electronics} -- the
repository's existing over-occupied cell, wearing a hardware costume.

---

## 2. Already done by someone else

Ideas dropped because materially equivalent work exists. Prior-art links are
mandatory. These are settled: do not re-search them without a specific reason to
think the landscape has changed, and if you do, record what changed.

### cron / crontab linter — rejected twice (2026-09-11, 2026-09-12)
Hook attempt: "checks your crontab for daylight-saving and escaping mistakes."
Considered independently on two runs, searched and rejected both times. Prior art:
[CronLens](https://github.com/SNO7E-G/CronLens) (lints cron expressions with DST,
overlap and thundering-herd warnings),
[cron-doctor](https://github.com/HeytalePazguato/cron-doctor) (ten lint checks),
[cronlint](https://github.com/zbcdo/cronlint), and `cronkit` (CLI crontab linting
with overlap detection and schedule projection). Same problem, same user, same
workflow. **Settled — do not consider a third time.** Also now inside the shape
ban.

### swapped-argument detector for Python — set aside (2026-09-12)
Hook attempt: "finds function calls whose arguments are in the wrong order."
Not built because the capability exists as research work, which would have capped
novelty confidence. Prior art: the DeepBugs IntelliJ plugin (incorrect function
arguments in Python), and
[eth-sri/learning-real-bug-detector](https://github.com/eth-sri/learning-real-bug-detector)
(argument-swap task). Also now inside the shape ban.

### CSV anti-join / join-diagnosis tool — rejected (2026-09-12)
Hook attempt: "tells you why your two spreadsheets didn't line up."
Prior art: Apify's CSV Anti-Join Finder, and the R package `joinspy`. Materially
equivalent.

### P2 — recovering a netlist from Gerber manufacturing files (2026-09-13)
Hook attempt: "Give it the files a factory uses to build a circuit board, and it
works out the wiring the designer drew."
Searched 2026-09-13: "recover netlist from Gerber files reverse engineering PCB
schematic reconstruction". **Materially equivalent prior art exists and it is
commercial and mature.** Altium Designer ships this as a documented workflow --
import the fabrication dataset into CAMtastic, assign layer types and drill sets,
*extract and validate connectivity*, export to a PCB document
(https://www.altium.com/documentation/knowledge-base/altium-designer/convert-gerber-odb-fabrication-data-back-to-pcb).
An entire service industry does it (https://reversepcb.com/gerber-to-pcb/,
https://iwdfsolutions.com/pcb-reverse-engineering/), and it is patented
(US 5781447, "System for recreating a printed circuit board from disjointly
formatted data"). Copper-polygon-to-connectivity is the solved part.
**Direction it leaves open, per the "what is the version of this that is not
done?" rule:** connectivity extraction is solved; *electrical interpretation* of
the recovered graph is not, and `IDEA_DOMAINS.md` D3 is explicit that this is the
distinguishing requirement. Any survivor here has to start after the netlist, not
at it.
Descriptor: {reads a file, fabrication data, netlist, electronics}.

### P3 — semantic structural diff for schematics and netlists (2026-09-13)
Hook attempt: "Shows you that someone added a pull-up resistor, instead of showing
you that line 4,812 of a file changed."
Searched 2026-09-13: "KiCad schematic semantic diff netlist structural diff tool
git version control hardware". This looked strong -- `AGENT_RULES.md` names "a
diff or merge strategy for something that currently has none" as a target, and
hardware people genuinely suffer here. **It is occupied.** KiHub
(https://kihub.dev/) advertises "visual and semantic diffs" that "trace component
changes from schematic to PCB", and frames the problem in the same words this
candidate did: a `.kicad_sch` diff shows that a value changed but not the affected
circuit, component, net or electrical context. CADLAB (https://cadlab.io/) sells
graphical version control for KiCad. KiRI (https://github.com/leoheck/kiri) and
kicad-diff-visualizer (https://github.com/uchan-nos/kicad-diff-visualizer) are
open-source, and KiCad has an upstream issue for it (kicad issue 2151).
**Honest residue:** KiRI and kicad-diff-visualizer are *image* diffs and do not do
topological matching, so the graph-level version is not fully claimed by the open
tools -- but KiHub claims the semantic framing directly, and a candidate whose
pitch is a funded product's marketing copy fails Gate E. Not settled to the degree
the cron linter is: if someone inspects KiHub directly and finds it is pixel
diffing with a better vocabulary, this can move back to section 5.
Descriptor: {compares two versions, design files, visual diff, electronics}.

### P4 — a canonical form for circuit topology (2026-09-13)
Hook attempt: "Two boards laid out completely differently get the same
fingerprint, because they are the same circuit."
Searched 2026-09-13: "circuit topology canonical form graph isomorphism subcircuit
search netlist fingerprint". This was the most attractive candidate in the pool on
the upstream-primitive rule -- it answers "what becomes buildable?" with a list
(dedup, clone detection, subcircuit search, library matching, diffing). **It is a
mature EDA field.** Canonical topology-only netlist normalisation with remapped
node identifiers and ground pinned to node 0 is standard practice; subcircuit
recognition is formally posed as bipartite subgraph isomorphism and is the basis
of layout-versus-schematic checking; there is GNN work on approximate subgraph
isomorphism for netlists (http://www2.ece.umn.edu/users/sachin/conf/date20.pdf)
and on functional matching beyond structural isomorphism
(https://arxiv.org/html/2505.21988); and it is patented (US 7441215, hierarchical
netlist comparison). Building it again is re-deriving LVS.
Descriptor: {computes an invariant, netlist, identifier, electronics}.

### P5 — thermal field computed from Gerber copper geometry (2026-09-13)
Hook attempt: "Reads the copper shapes a factory would print and shows you where
the board will get hot."
Searched 2026-09-13: "thermal simulation from Gerber copper pour geometry open
source PCB heat map hobbyist". **Occupied at both ends.** Commercial tools import
Gerber/ODB++ for thermal analysis directly (Altium, Ansys Icepak), KiCad covers
basic copper-plane and thermal-via modelling, and there is a documented
open-source route through Elmer and ParaView
(https://jrainimo.com/build/2024/11/oss-thermal-simulation-of-pcbs/). The gap is
convenience, which is R7 ("nicer UX" is not a project).
Descriptor: {simulates, fabrication geometry, heat map, electronics}.

### P14 — an explorable schematic you probe by clicking nodes (2026-09-13)
Hook attempt: "Click any wire in the circuit and watch the voltage move."
**Rejected on prior art, immediately and without a web search**, because the prior
art is famous: Paul Falstad's circuit simulator (https://www.falstad.com/circuit/)
has done exactly this in a browser for roughly two decades, with animated charge
flow and live probing, and there is a maintained fork (circuitjs). Materially
equivalent. Recorded so no future run re-derives it from the
"explorable explanations" line in `REFERENCES.md`.
Descriptor: {click and probe, circuit model, interactive canvas, electronics}.

### P17 — structure recovery from public firmware dump archives (2026-09-13)
Hook attempt: "Point it at an unknown firmware blob and it maps out what is inside."
**Rejected on prior art without a dedicated search**: this is what binwalk,
Ghidra, unblob and the whole firmware-analysis toolchain already do, and the field
is crowded with both open-source and commercial entrants. Kept as a record so the
"unexploited dataset" line of generation does not produce it again.
Descriptor: {reads a blob, firmware image, structure report, security tooling}.

---

## 3. Not hyped — passed the other rules, failed the hook

**This section is a resource, not a graveyard.** These ideas are real, buildable,
unclaimed, and satisfy the rules on problem value, feasibility, originality and
completeness. They failed only Gate F: no hook sentence a stranger would repeat,
or nothing that can be shown in ten seconds.

They are kept because a hook can be found later. An idea moves to section 4 when
someone writes a hook sentence that genuinely passes all four tests — surprising,
concrete, context-free, not a category label — or when the framing changes so that
the interesting part becomes the project. Very often the fix is scope, not
wording: the boring application was hiding a primitive worth building on its own.

Record for each: the hook attempts that failed, and what would have to be true for
it to become hyped.

### backfire (built 2026-09-11, `projects/backfire/`) — belongs here by today's rules
"Finds retry amplification and timeout blowups in Python codebases." Genuinely
useful, honestly validated, 85 tests. Fails Gate F: a category label, no demo, and
inside the shape ban. What would make it hyped: the composed-retry-multiplication
result shown **visually** — a diagram or animation of one click fanning out into
thirty requests across the call graph. The engine is interesting; the CLI report
hides it.

### orbiter (built 2026-09-12, `projects/orbiter/`) — belongs here by today's rules
"Flags Python code that mixes units, like milliseconds passed as seconds." Strong
validation, 151 tests, real controls. Fails Gate F for the same reasons. What
would make it hyped: unit inference as something you can *see* — units propagating
through an expression live as you type, rather than a warning printed after.

---

## 4. Hyped and selected — building, or built

Ideas that passed every gate including Gate F, with a hook sentence that holds.
Each entry keeps its hook sentence verbatim, its status, and a link to its folder.
An entry stays here after completion; this doubles as the repository's back
catalogue.

### cutline (built 2026-09-12, `projects/cutline/`) — partially qualifies
Shipped as: "Reads one plain-text plan and decides whether everything fits."
Contains a genuinely strong idea that was not surfaced: an engine that **proves**
a set of commitments cannot all be met, emits a certificate you can check by hand,
and computes the provably cheapest subset to drop — verified against exhaustive
enumeration, 200 of 200. Better hook, available the whole time: *"Proves your plan
is impossible, then tells you the single cheapest thing to drop."* That engine
generalises to sprints, cloud budgets, timetables and CI minutes, and should have
been the project with the planner as one demo. Recorded as the worked example of
the ship-the-primitive rule.

_No project currently selected. The next entry here is the first one chosen under
the full rule set, and it should be the best idea this repository can find rather
than the first that qualifies._

---

## 5. Live pool — generated, still standing, not yet good enough

Candidates from the 2026-09-13 generation round that survive the hard filters and
the gates so far, but have **not** been selected. Selection spans runs by design
(`AGENT_RULES.md`, "sleep on it"), and on this run's evidence nothing here has
reached the bar: *good enough that I would be disappointed to see someone else
ship it first*. Four of the strongest candidates from the same round were killed
outright on prior art and are in section 2 above.

The next run re-reads this section **before** generating anything new. An entry
that still reads well after the gap is a real candidate; one that does not was
infatuation.

### P1 — recovering an unknown wire protocol from raw captures, and emitting a decoder
Hook attempt: *"Point it at a recording of two chips talking, and it works out the
language they invented and writes you the decoder."*
Descriptor: {analyses a signal, raw logic capture, synthesised decoder code,
electronics + reverse engineering}. Cross-domain D1 x D3, which
`IDEA_DOMAINS.md` section 0.2 explicitly prefers.
If this works, what becomes buildable: anything downstream of "I can read this
bus" -- interoperating with an undocumented device, writing a sigrok decoder
without doing it by hand, checking a device still speaks what it used to.

Searched 2026-09-13, two formulations plus two on the adjacent field:
- "infer unknown digital protocol from logic analyzer capture automatically
  synthesize decoder" -- found manual and semi-automated decoder writing for
  sigrok, and one narrow automatic inference result (the `can2` decoder inferring
  a CAN frame's sender from deterministic signal distortion,
  https://kentindell.github.io/2023/04/21/can2-decoder-update/). No
  general-purpose synthesiser surfaced.
- "sigrok automatic protocol detection unknown signal classify I2C SPI UART from
  raw trace research" -- **this kills the classification framing.** Deciding
  whether a capture is UART, I2C or SPI is patented (US 12282446, US 12132810) and
  implemented; UART by idle state, SPI by slave-select toggling, I2C by continuous
  clock activity. Any version of this that merely identifies a *known* protocol is
  dead on arrival.
- "automatic protocol reverse engineering survey Netzob Discoverer BinaryInferno
  NetPlier inference of message format" -- a large, mature academic field:
  the Sija 2018 survey (https://onlinelibrary.wiley.com/doi/10.1155/2018/8370341),
  Netzob (sequence alignment over messages), Discoverer, NetPlier
  (https://www.ndss-symposium.org/wp-content/uploads/ndss2021_4A-5_24531_paper.pdf),
  state-machine inference (https://arxiv.org/pdf/2412.02540), and a curated list
  at https://github.com/techge/PRE-list.
- "physical layer protocol reverse engineering raw waveform unknown encoding
  Manchester NRZ recover framing bit rate blind" -- blind physical-layer recovery
  and blind frame synchronisation are established in the **RF / non-cooperative
  communications** literature (https://arxiv.org/pdf/1704.05432).

**The one real gap, stated precisely so the next run can attack or discard it:**
every tool in the academic protocol-reverse-engineering field takes *already-framed
byte messages* as input -- network traces, where message boundaries are given. The
physical-layer literature that does work below that line is RF-flavoured. The
wired-embedded case, starting from sampled logic levels with no knowledge of which
line is the clock, no bit rate, no encoding and no framing, and ending in a
*runnable decoder*, is where the two bodies of work do not meet.
**Ground truth: resolved, and it is real.** Checked later in the same run.
`sigrok-dumps` (https://github.com/sigrokproject/sigrok-dumps, mirror of
git://sigrok.org/sigrok-dumps) is a corpus of **real** logic-analyser captures --
not synthesised -- organised into **60+ protocol directories** (i2c, spi, uart,
can, jtag, onewire, ps2, usb, dali, dcc, dmx512, flexray, sent, swd, swim,
wiegand, morse, miller, graycode, nonstandard_eeproms, misc and many more), in
sigrok's `.sr` session format, and **released into the public domain by their
authors** unless noted otherwise. Public domain matters twice here: it satisfies
the lawfully-obtained-artifacts constraint in the reverse-engineering section of
`AGENT_RULES.md`, and it removes any terms-of-service question.

**The evaluation design this makes possible**, which is the part that lifts
verifiability: hold out the directory label, feed the system only raw samples, and
require it to recover which line is the clock, the bit rate, the encoding and the
framing with no knowledge of protocol identity. Score the recovered framing
against sigrok's own reference decoder output for that capture. Evaluating on
*known* protocols is not a contradiction of the unknown-protocol framing -- it is
the only way to get ground truth, and it is sound precisely because the method is
forbidden to use the identity.

**Live risk that remains:** the gap may be an artefact of my search terms rather
than the world. `AGENT_RULES.md` warns that genuinely empty regions are rarer than
they look, and the honest prior is that some of this is covered somewhere I did
not look. Another search round is warranted before committing, not after.

Scores (hook 4, reach 4, demo-ability 4, originality 3, difficulty-worth-it 4,
monetizability 3; verifiability 4 after the corpus check). Originality stays 3,
not higher, because of the RF blind-recovery literature. Under `IDEA_DOMAINS.md`
section 3 this clears verifiability >= 4 but sits **below the novelty >= 4
requirement**, and that is the single thing standing between it and selection.
Resolving it means either finding the framing that makes it genuinely a 4, or
dropping the candidate. Do not round a 3 up.

### Red team on P1, written before any implementation

*The closest existing thing.* sigrok's own decoder collection -- over a hundred
hand-written decoders covering essentially every protocol in the corpus. Then the
academic protocol-reverse-engineering field for message formats, and the RF blind
demodulation and blind frame synchronisation literature for the physical layer.
Auto-detecting which of UART/I2C/SPI a capture is, is patented and shipped.

*Why a stranger would shrug.* "My logic analyser already decodes I2C." That
objection is fatal to the wrong version of this project, and it has to be answered
by the demo rather than by prose: the demo has to be a bus for which **no decoder
exists**, where the tool produces a runnable one. On a known protocol this will
always look like a worse version of a decoder someone already wrote by hand, and
any demo on I2C is a demo of the wrong thing.

*The part only interesting to its author.* The clock-recovery and encoding
inference machinery. It is the intellectually satisfying half and a stranger does
not care about it at all; they care whether a decoder came out and whether it
works.

*Answering the objections, honestly.* The first is answerable only by finding a
genuinely undocumented capture to demo on. The `nonstandard_eeproms` and `misc`
directories are the obvious place to look and **that check has not been done**. If
no such capture can be found, the demo collapses to "reproduces decoders that
already exist", the hook stops being literally true, and the candidate should be
dropped rather than shipped with a quieter claim. The second objection is
answerable by scope discipline: the deliverable is the emitted decoder and the
inference machinery is the implementation. **The first objection is real and I
cannot fully answer it yet** -- `AGENT_RULES.md` says an unanswered objection
becomes the first thing a reader notices later, so it is recorded as open, not as
settled.

### P7 — a representation for a circuit you only partly know
Hook attempt: *"A wiring diagram that can say 'I cannot tell' about one specific
wire, and be right about how sure it is."*
Descriptor: {represents and combines evidence, partial observations, data
structure plus a viewer, electronics}. This is the upstream-primitive candidate of
the round.
If this works, what becomes buildable: every D3 project needs it. `IDEA_DOMAINS.md`
D3 demands calibrated per-net, per-component confidence and the ability to say
"undetermined from the available images", and there is no standard structure for
a partially-known netlist -- existing formats assert connectivity as fact. A
board reconstructed from photographs, from Gerbers, and from X-ray would each be
partial evidence this could merge.
**Searched once, 2026-09-13**: "representation for partially known netlist
uncertainty per-net confidence probabilistic circuit reconstruction calibrated".
**No materially equivalent prior art surfaced** -- but treat that as weak
evidence, for one specific and recordable reason: **the terminology collides.**
"Probabilistic circuit" is an established term for something entirely different,
a tractable probabilistic model class in the sum-product-network family
(https://arxiv.org/abs/2302.06544, and Van den Broeck's IJCAI-20 tutorial), and it
swamps the query. The only genuinely adjacent hit -- probabilistic reconstruction
of a network from partial knowledge -- is from gene regulatory networks
(https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3236852/), not electronics.
A future search has to route around the collision: try "netlist confidence",
"uncertain connectivity", "partial netlist extraction", "LVS with unknowns", and
the PCB-reverse-engineering vocabulary rather than the machine-learning
vocabulary. Until that is done this is unsearched in substance.
It remains the highest-value open entry in the pool on the upstream-primitive
rule, because it is the one candidate that answers "what becomes buildable?" with
a list rather than a use case.
**Known risk before searching:** it may collapse into "a netlist with confidence
floats attached", which is a data schema, not an invention. What would make it
real is the *evidence-combination algebra* -- what happens when two images
disagree, when a trace vanishes under a chip, when a via implies connectivity that
is not visible -- and whether the confidences come out calibrated against ground
truth rather than asserted. If that part is not substantial, this fails Gate A.
Scores: not yet scored; scoring it before searching it would be theatre.

### P6, P12 — a type system for electrical connections
Hook attempt: *"It knows that connecting these two pins destroys both chips,
for the same reason a compiler knows you cannot add a number to a date."*
Descriptor: {checks a model, netlist, diagnostic, electronics + language design}.
Cross-domain transplant: types and abstract interpretation, taken from programming
languages into electrical nets -- voltage domain, drive strength, direction and
bus discipline as a type lattice.
**Two unresolved problems, both serious.** Prior art: KiCad and every EDA suite
ship an electrical rule check that does a weaker version of this, so the candidate
has to be about the *lattice and its soundness*, not the warnings. And the shape
ban: as an application it is a checker that reads a file and prints findings,
which is banned, and P24 above was rejected for exactly that. It survives only if
the type system itself is the deliverable -- with a soundness argument and
exhaustive tests over a generated space of circuits -- and the checker is one
demo of it. That is the ship-the-primitive rule applied honestly, and it is a
genuinely harder project than it first looks.
Scores: not yet scored, pending the prior-art search on ERC formalisation.

### P8 — reconstructing a board from photographs
The `IDEA_DOMAINS.md` D3 headline. Not rejected, not advanced. **The blocker is
ground truth, and it is specific:** the evaluation needs boards where photographs
*and* authoritative design files both exist and correspond, and D3 is explicit
that without a ground-truth set this is a demo and should not be selected.
Open-hardware projects publish design files reliably and photographs
inconsistently, and a photograph of a board is often of a different revision than
the published files. Next step if pursued: establish whether a corpus of even
twenty paired board photo sets and design files can actually be assembled, before
any modelling work. That check is cheap and decides the candidate.

### P9, P10 — turning a datasheet into something executable
P9: a timing diagram in a datasheet image becomes machine-checkable timing
assertions. P10: a register table becomes a driver plus the property test that
proves the driver matches the table.
Both are D1 in the preferred form -- machine-readable in, machine-readable out,
output is an executable check rather than prose. **Both need the R2 subtractive
test applied honestly before going further**, and P10 probably fails it: delete
the model call from "read a register table, emit a driver" and there may be
nothing but prompt plumbing left. P9 survives that test better, because reading
geometry out of a rendered timing diagram is real image work.
Not searched.

### P25 — a structural diff for two signal captures
Hook attempt: *"Shows you what the device did differently this time."*
Descriptor: {compares two recordings, logic capture, aligned visual diff,
electronics}. Generated late, unsearched, and noted here mainly because it shares
machinery with P1 -- alignment and framing recovery -- and might be the cheaper
vertical slice of the same underlying work.

### P15, P16, P23, P26 — generated, recorded, not developed
P15: public SDR/RF recording archives as an unexploited dataset. P16: government
sensor archives (seismic, tide gauge) as an unexploited dataset -- too vague to be
a candidate as stated, and recorded to stop it being re-generated in the same
vague form. P23: inferring what a circuit *does* (this is a buck converter, this
pair is a decoupling path) from a netlist -- overlaps the GNN netlist-recognition
prior art found under P4 and would need to clear it. P26: sequence alignment from
bioinformatics applied at the *bit* level to logic captures -- Netzob already
applies Needleman-Wunsch at the byte level to network messages, so this is a
component of P1 rather than a candidate of its own.

---

## 6. Selection status, 2026-09-13

**Pool size this round: 36 candidates** -- C1-C10 from the owner's external
analysis, P1-P26 generated here. That clears the 20-candidate quota.
**Resolved this round: 22.** Ten on `IDEA_DOMAINS.md` section 0.3, five on R4/R6
feasibility, three on the gates (Gate A, Gate D, shape ban), six on prior art
(sections 2, P2/P3/P4/P5/P14/P17). **Standing: 14, none selected.**

**The first idea generated this round was P2 (Gerber to netlist), and it was
rejected**, per the rule requiring the first idea to be rejected as a final
answer. It then died independently on prior art, which is a fair indication the
rule is pointing at something real.

**Why nothing was selected.** The two candidates that scored best on the
upstream-primitive rule -- P4 (canonical circuit fingerprint) and P3 (semantic
netlist diff) -- both turned out to be occupied, one by a mature EDA field and one
by a funded product using the same framing.

P1 is the provisional front-runner and its ground-truth dependency was resolved
favourably later in the run: `sigrok-dumps` is real, public domain, 60+ protocol
directories of genuine captures, and supports a held-out evaluation that lifts
verifiability to 4. **Two things still stand between it and selection**, and
neither is a formality:

1. **Novelty is a 3, and `IDEA_DOMAINS.md` section 3 requires >= 4.** The RF
   blind-recovery literature is the reason. Either a framing is found that makes it
   honestly a 4, or the candidate is dropped. Rounding a 3 up to clear a threshold
   would be exactly the fabricated-score failure the rules warn about.
2. **The red-team objection is unanswered.** The demo needs a capture of a bus with
   no existing decoder. If every capture in the corpus already has a hand-written
   sigrok decoder, the demo becomes "reproduces what exists", the hook stops being
   literally true, and the candidate dies. Whether such a capture exists was not
   checked.

Selecting P1 now would be choosing the best candidate on the current list, which
`AGENT_RULES.md` explicitly forbids, rather than one I would be disappointed to
see someone else ship first. It is close. It is not there.

**Pairwise comparison, top two.** P1 against P7, on "which would I be more upset
to see someone else ship first": **P7**. A working representation for a
partly-known circuit with a calibrated evidence algebra would be the thing other
people's board-reconstruction work gets built out of, and P1 would be one of its
consumers. P1 wins on demo-ability and on being nearly ready to start; P7 wins on
the question the rules say does the most work. That is the strongest argument for
spending the next run's search on P7 rather than starting P1 because it is
available -- "you are choosing it because it is clearly finishable" is the listed
signal of rushing, and P1 is the candidate that triggers it.

**The honest structural observation, for the owner.** Every surviving candidate
sits in electronics. That is a direct consequence of the filters rather than a
free choice: R1-R5 remove the conversational and wrapper shapes, R6 removes D2 and
D5 in this container, R4 and section 0.3 remove D4, and the `AGENT_RULES.md` shape
ban removes the checker skeleton the repository keeps defaulting to. What remains
is D1 and D3, and D3 is where the interesting cross-domain work lives. Worth
knowing that the domain concentration is the rules working as written, and worth
the owner's attention if it was not intended.
