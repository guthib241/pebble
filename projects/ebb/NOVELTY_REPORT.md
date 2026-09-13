# Novelty report — ebb

**Project**: `ebb`

**One-sentence description**: A 2D physics simulation that runs backwards bit-for-bit without stored frames.

**Date of search**: 2026-09-13

---

## Search scope

The claim under test is **not** "bit-reversible integration is new" — it is not. The claim
under test is:

> An integer-arithmetic 2D simulation with **collisions and contact** whose step is a
> bijection on the state, so the simulation can be stepped backwards to reproduce every
> earlier frame bit-for-bit without storing frames, shipped as a runnable engine with a
> visible rewind.

So the search covered four separate literatures that each own a piece of this, to
establish whether any of them already owns the whole of it:

1. bit-reversible / time-reversible numerical integrators (molecular dynamics, N-body,
   graphics);
2. reversible computing and reverse computation in parallel discrete-event simulation,
   specifically for collisions;
3. deterministic game-physics engines and rollback/rewind practice (where rewind is the
   stated goal);
4. physics of reversibility in frictional and granular contact (to establish whether
   exactly reversible dissipative contact is even coherent).

### Sources searched

* **Academic**: arXiv (physics.comp-ph, cs.CG, cond-mat), Springer, ScienceDirect,
  ResearchGate, ADS, OSTI, NVIDIA Research publications.
* **Public source repositories**: GitHub (repository search and topic pages
  `physics-engine`, `rigid-bodies`, `rigid-body-dynamics`, `rollback-netcode`), GitLab
  (Snopek Games SG Physics 2D).
* **Package registries**: npm (`@dimforge/rapier2d`, `@dimforge/rapier2d-deterministic`,
  `@rpgjs/physic`, npm "physics engine" search), PyPI-indexed Python engines surfaced via
  search (PhysEng, Simulation-Engine, PyChrono, SOFA).
* **Developer forums and discussion**: GameDev.net (deterministic physics replay; time
  reversal in real-time 3D), DEV Community, Hacker News, itch.io developer posts and
  devlogs, BEPUphysics forum.
* **Issue trackers / project discussions**: JoltPhysics discussion #1034 ("Efficient
  rollbacks to support predict-rollback netcode").
* **Product documentation**: Rapier determinism documentation, Matter.js, propel-js.

### Query formulations used (verbatim)

1. `exactly time-reversible physics engine integer arithmetic bit-reversible rewind simulation without saving states`
2. `reversible physics engine game rewind without snapshots "run the simulation backwards" deterministic integer rigid body collisions`
3. `time-reversible collision resolution rigid body simulation exactly invertible discrete dynamics github`
4. `event-driven hard sphere molecular dynamics exact rational arithmetic time reversible collisions exactly invertible`
5. `rollback netcode rewind by re-simulating backwards instead of storing snapshots reversible game state`
6. `"reversible physics engine" OR "reversible simulation" python package npm library github rewind bit-exact`
7. `fixed-point deterministic lockstep physics engine integer math rewind rollback gamedev discussion reverse time exactly`
8. `reversible contact dynamics friction restitution "time reversal" information loss store residue bits rewind simulation research`
9. `game engine "reverse simulation" rewind by running physics backwards itch.io prototype reversible billiards demo`
10. `"reverse computation" reversible discrete event simulation billiards elastic collision Perumalla implementation library`

Alternate terminology considered and searched through the formulations above:
*bit-reversible*, *bitwise reversible*, *time-reversible*, *invertible dynamics*,
*reverse computation*, *retrodiction*, *rollback*, *rewind*, *fixed-point*, *lockstep
determinism*, *hard-sphere event-driven*, *unfolding*.

---

## Closest prior art

### 1. Jos Stam, *An Exact Bitwise Reversible Integrator* (NVIDIA, arXiv:2207.07695, 2022)

The closest match on mechanism. Integrates Hamiltonian systems in fixed-point
(i.e. integer) arithmetic so that "integrating forward for an arbitrary number of time
steps and then backward recovers any previous state exactly at a bitwise level". It even
names the rewind application: "animators can browse back and forth in time to refine a
simulation's results."

Inspected directly: the PDF was downloaded and its text extracted
(`research.nvidia.com/labs/prl/stam2023reversible/reversible2022.pdf`). Across the full
text, the words *collision*, *contact*, *rigid*, *impact*, *wall*, *bounce* and
*friction* occur **zero** times; *constraint* occurs once, in the adjoint-method sense
(`E = y − f(x) = 0`). Its stated main application is the reverse step of the adjoint
method in optimization and backpropagation.

### 2. Kalyan S. Perumalla and Vladimir A. Protopopescu, *Reversible Simulations of Elastic Collisions* (ORNL, arXiv:1302.1126, 2013)

The closest match on the collision problem specifically. Abstract, read directly from the
extracted PDF text: "Consider a system of N identical hard spherical particles moving in
a d-dimensional box and undergoing elastic, possibly multi-particle, collisions. We
develop a new algorithm that recovers the pre-collision state from the post-collision
state of the system, across a series of consecutive collisions, with essentially no
memory overhead." Reversibility is obtained by pseudo-randomizing the free collision
angles so the reverse path is reproducible; perfect reversibility of collisions is
reported for restricted cases (n ≤ 3 in 2D, n = 2 in 3D). The context is reverse
computation for optimistic parallel discrete-event simulation.

Identical hard spheres only: no rotation, no polygons, no resting contact or stacking, no
friction or restitution, and the arithmetic is not an integer state space.

### 3. Bit-reversible integrators in molecular dynamics and N-body

Levesque & Verlet's integer leapfrog (the original bit-reversible MD integrator), the
bit-reversible Milne fourth-order integrator (arXiv:1706.08678), Hoover's
time-reversible continuum mechanics work, and **JANUS** (Rein & Tamayo, arXiv:1704.07715),
a bit-wise reversible integer integrator for N-body dynamics. All are smooth-force
systems — gravitational or potential-gradient forces — with no contact events.

### 4. Deterministic game-physics engines with snapshot rewind

SG Physics 2D (fixed-point deterministic 2D physics for Godot), Rapier's
`-deterministic` builds, propel-js, `@rpgjs/physic` (explicitly "includes snapshot/restore
functionality for rewinding"), and the Jolt discussion on efficient rollbacks. These are
the closest match on **use case**. Every one of them achieves rewind by storing and
restoring state: determinism makes replay *forward* from a stored state reproducible. None
claims an invertible step.

### 5. Game-development rewind practice

itch.io devlog "Time rewinding mechanic tutorial" (rewind by recording per-object state),
GameDev.net "Time Reversal in Real-Time 3D", which states the position plainly: there is
no general way to treat all operations by simply reversing them, and the practical route
is to record state or inputs and play them back.

### 6. Exact-arithmetic game physics

The "Perfect, Infinite-Precision, Game Physics in Python" series keeps positions and
velocities as exact symbolic expressions to avoid floating-point drift. Exactness without
reversibility: the state representation grows with the simulation, and no invertible step
is claimed.

### 7. Physics of reversible contact (bounding what is achievable)

"Reversibility of granular rotations and translations" (arXiv:1810.12985) reports that the
rolling/slipping transition in frictional contact is hysteretic, so conserving contact
points does not guarantee reversal of rotational motion; "Shannon information increase and
rescue in friction" frames friction as information loss below a coarse-graining scale.
These are treated here as constraints on the design, not as prior art on the artifact:
they are why `ebb` makes information that contact destroys **explicit and stored**, rather
than claiming dissipative contact is reversible for free.

---

## Feature-level comparison

| Dimension | ebb (proposed) | Stam 2022 | Perumalla & Protopopescu 2013 | Deterministic game engines (Rapier/SG/propel) |
| --- | --- | --- | --- | --- |
| Problem | Step a contact simulation backwards exactly, without stored frames | Exact reverse step for the adjoint method | Recover pre-collision state in optimistic PDES | Reproduce a simulation across machines; rewind for netcode |
| User | People who want rewind, replay or rollback of an interactive simulation | Optimization / ML researchers | PDES researchers | Game developers |
| Inputs | A scene of bodies, integer state | Hamiltonian system, fixed-point state | N identical hard spheres in a box | A scene plus stored snapshots |
| Core mechanism | Every step is a bijection on integer state; contact resolved by self-inverse mirror rules; information that rounding or dissipation would destroy is written to a small residue tape | Fixed-point integration of smooth forces | Pseudo-randomized collision angles reconstructed in reverse | Fixed-point/deterministic floating point, plus snapshot & restore |
| Collisions / contact | Central: walls, body-body, later rotation, stacking, friction | Absent | Elastic hard-sphere collisions only; n ≤ 3 in 2D | Central, but not invertible |
| Workflow | Step forward; step backward; land on the exact earlier frame | Integrate forward, then backward, for gradients | Roll back events during PDES execution | Store a frame, later restore it and replay forward |
| Storage for rewind | No frames; a residue tape measured in bits per contact event | None (smooth forces) | "Essentially no memory overhead" | One state per rewindable frame |
| Outputs | Frames, demos, an interactive scrub that plays backwards | Gradients | Reversed event stream | Rendered game frames |
| Deployment | Self-contained library plus committed animated demos and a browser page | Research paper | Research paper | Production engines |
| Distinguishing capability | Reversible **contact** dynamics as a usable engine, with the cost of reversing dissipation measured rather than assumed | Reversible smooth dynamics | Reversible elastic sphere collisions in a restricted regime | Deterministic forward replay from stored state |

## Material equivalence assessment

No source found provides materially the same core capability through substantially the
same workflow. The two closest items each own one half and explicitly not the other:
Stam 2022 owns exact integer reversibility but contains no contact at all; Perumalla &
Protopopescu own collision reversal but for identical frictionless hard spheres in a
restricted regime, without an integer state space, rotation, polygons, stacking or a
usable engine. The engines that own the use case obtain rewind by storing state, which is
the thing `ebb` exists to avoid.

Components of `ebb` certainly exist already: fixed-point arithmetic, integer leapfrog,
mirror reflection by unfolding, impulse-based collision response. Per the material
equivalence test, existing components do not eliminate capability-level novelty, and the
assembled capability — *contact dynamics whose step is invertible, with the residue cost
of reversing dissipation measured* — was not found.

## Unresolved uncertainty

* Reversible computing and PDES literature is large, and some of it is in proceedings not
  well indexed by general search. A reversible contact-dynamics result may exist there
  under terminology not covered by the ten queries above.
* Game and demo scenes are largely unindexed. A hobby project implementing an invertible
  contact step may exist on itch.io or in a game jam entry without describing it in those
  words.
* Lattice-gas and reversible cellular automata models (HPP, FHP, Margolus neighbourhoods)
  achieve exact reversibility for collision-like interactions by construction. They are a
  different model of dynamics rather than a contact engine, so they are not counted as
  materially equivalent — but they are genuine evidence that exact reversibility of
  collision-like rules is known, and they cap the novelty of the idea that it is possible
  at all.
* The distinguishing capability is partly a claim about what `ebb` will do at later
  milestones (rotation, stacking, friction). Until those exist, the comparison above
  should be read as describing the **project**, with the README stating what is
  implemented today.

## Novelty confidence

**Medium.**

Multiple source categories were searched with ten query formulations, and the two
strongest matches were inspected directly at full text. Medium rather than High because
the mechanism (integer arithmetic giving a bijective step) is established prior art that
`ebb` deliberately reuses, because reversible-computing proceedings are imperfectly
indexed, and because unindexed game-jam work cannot be ruled out.

This conclusion is limited to the sources and queries documented above. It is a
search-based estimate, not a statement that no equivalent work exists.
