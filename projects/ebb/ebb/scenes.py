"""Named scenes, so the demo, the tests and the evidence run the same worlds.

Every scene is fully determined by its seed: no wall-clock time, no process state.
"""

import random

from .world import World

BOX = (0.0, 0.0, 12.0, 8.0)


def _place(world, rnd, radius, margin=0.05, tries=400):
    """Find a spot for a disc that does not overlap the discs already placed.

    Scenes must not start in interpenetration. Milestone 1 resolves contact by
    exchanging normal velocity, and a pair that begins overlapped can take many
    steps to separate, which is a property of the starting state rather than of
    the dynamics. Starting apart keeps the two separable.
    """
    x0, y0, x1, y1 = BOX
    for _ in range(tries):
        x = rnd.uniform(x0 + radius + margin, x1 - radius - margin)
        y = rnd.uniform(y0 + radius + margin, y1 - radius - margin)
        for j in range(len(world)):
            dx = x - world.x[j] / 65536.0
            dy = y - world.y[j] / 65536.0
            reach = radius + world.r[j] / 65536.0 + margin
            if dx * dx + dy * dy < reach * reach:
                break
        else:
            return x, y
    raise RuntimeError("could not place a disc without overlapping: scene is too full")


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
        x, y = _place(w, rnd, radius)
        w.add_disc_units(x, y, rnd.uniform(-0.06, 0.06), rnd.uniform(-0.06, 0.06), radius)
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
        x, y = _place(w, rnd, radius)
        w.add_disc_units(x, y, rnd.uniform(-0.05, 0.05), rnd.uniform(-0.05, 0.05), radius)
    return w


SCENES = {"drop": drop, "billiards": billiards, "single": single, "scatter": scatter}
