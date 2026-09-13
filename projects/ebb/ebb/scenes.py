"""Named scenes, so the demo, the tests and the evidence run the same worlds.

Every scene is fully determined by its seed: no wall-clock time, no process state.
"""

import random

from .world import World

BOX = (0.0, 0.0, 12.0, 8.0)


def drop(seed=7, n=8, gravity=0.004, radius=0.42):
    """A handful of balls let go near the top of a box, under gravity."""
    rnd = random.Random(seed)
    w = World.from_units(BOX, gravity=(0.0, -gravity))
    for i in range(n):
        x = 1.2 + i * (9.6 / max(1, n - 1))
        y = 6.6 + 0.18 * rnd.uniform(-1, 1)
        w.add_disc_units(x, y, rnd.uniform(-0.02, 0.02), 0.0, radius)
    return w


def billiards(seed=3, n=6, radius=0.4):
    """No gravity, elastic contact only: the control scene for energy and tape."""
    rnd = random.Random(seed)
    w = World.from_units(BOX, gravity=(0.0, 0.0))
    for _ in range(n):
        w.add_disc_units(
            rnd.uniform(1.0, 11.0), rnd.uniform(1.0, 7.0),
            rnd.uniform(-0.06, 0.06), rnd.uniform(-0.06, 0.06), radius,
        )
    return w


def single(seed=0, gravity=0.004, radius=0.5):
    """One ball, so no pair ever contacts: the scene whose tape must stay empty."""
    w = World.from_units(BOX, gravity=(0.0, -gravity))
    w.add_disc_units(2.5, 6.0, 0.035, 0.0, radius)
    return w


def scatter(seed=11, n=14, radius=0.3):
    """More bodies than the others, for stress and timing."""
    rnd = random.Random(seed)
    w = World.from_units(BOX, gravity=(0.0, -0.002))
    for _ in range(n):
        w.add_disc_units(
            rnd.uniform(0.8, 11.2), rnd.uniform(0.8, 7.2),
            rnd.uniform(-0.05, 0.05), rnd.uniform(-0.05, 0.05), radius,
        )
    return w


SCENES = {"drop": drop, "billiards": billiards, "single": single, "scatter": scatter}
