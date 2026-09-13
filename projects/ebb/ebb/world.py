"""The reversible kernel: discs in a box, stepped forwards or backwards.

The whole design rests on one idea. A step is built only out of pieces that are
bijections on the integer state, so the step itself is a bijection and has an exact
inverse. Concretely, one step is:

1. **kick** -- ``v += g``. Depends only on the velocity's own previous value and a
   constant, so subtracting the same constant inverts it.
2. **drift with walls** -- ``x += v``, then mirror the result back inside the box if
   it left. Depends only on ``v``. The mirror is made invertible by reflecting about
   the half-unit *just outside* the wall rather than about the wall itself; see
   ``drift_axis``.
3. **contact** -- for every overlapping pair of discs, exchange the component of
   relative velocity along the line of centres. Positions are untouched, so the set
   of overlapping pairs is identical before and after, which is what lets the
   backward pass find exactly the pairs the forward pass resolved. Integer division
   destroys a little information here, and that -- and only that -- is written to a
   residue tape.

``step()`` and ``unstep()`` are exact inverses: ``unstep`` after ``step`` restores
every integer in the state. Nothing about intermediate frames is stored.
"""

from .fixed import SCALE, fx, varint_len


class TooFast(Exception):
    """A body moved further in one step than the box is wide.

    The mirror rule folds a body back in once per axis per step. A body that would
    cross both walls of an axis in a single step cannot be folded back by one
    reflection, so the state would leave the box and reversibility would be lost.
    Raised rather than silently clamped: clamping is not invertible.
    """


class TapeError(Exception):
    """``unstep`` was called with a residue tape that does not match the state."""


def drift_axis(x, v, lo, hi):
    """One axis of drift plus wall reflection. Returns ``(x, v)``.

    The naive mirror rule ``x' = 2*hi - (x + v)`` is *not* injective on the integer
    lattice: a body sitting exactly on the wall moving outwards and the same body
    moving inwards can land on the same state. Reflecting about the half-unit
    outside the wall (``2*hi + 1 - t``) separates the two cases completely:

    * no reflection  => ``x' - v'`` lies in ``[lo, hi]``
    * reflected at hi => ``x' - v' > hi``
    * reflected at lo => ``x' - v' < lo``

    Those three ranges are disjoint, so ``undrift_axis`` can tell which happened
    from the post-state alone, with nothing stored.
    """
    t = x + v
    if t > hi:
        x = 2 * hi + 1 - t
        v = -v
    elif t < lo:
        x = 2 * lo - 1 - t
        v = -v
    else:
        x = t
    if x < lo or x > hi:
        raise TooFast(
            "a body crossed the whole box in one step: |v| must be <= (hi - lo)"
        )
    return x, v


def undrift_axis(x, v, lo, hi):
    """Exact inverse of :func:`drift_axis`."""
    u = x - v
    if u > hi:
        return 2 * hi + 1 - u, -v
    if u < lo:
        return 2 * lo - 1 - u, -v
    return u, v


class Tape:
    """The residue tape: the only thing kept in order to go backwards.

    Contact resolution divides by the squared distance between two centres. Integer
    division throws away a remainder, and a step that throws information away is not
    invertible, so one integer per resolved contact is pushed here. It is a stack:
    the backward pass pops in reverse order.

    It holds nothing per frame and nothing per body -- only per contact event.
    """

    __slots__ = ("items",)

    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        if not self.items:
            raise TapeError("residue tape is empty: nothing left to step back over")
        return self.items.pop()

    def __len__(self):
        return len(self.items)

    def bytes_serialised(self):
        """Size of the tape as a zigzag-varint byte stream."""
        return sum(varint_len(v) for v in self.items)

    def bits_serialised(self):
        return 8 * self.bytes_serialised()


class World:
    """Discs in a box under constant gravity, in integer sub-units.

    Positions ``x``, ``y``, velocities ``vx``, ``vy`` and radii ``r`` are all ints.
    ``box`` is ``(x0, y0, x1, y1)`` in sub-units and is where the walls are.
    """

    def __init__(self, box, gravity=(0, 0)):
        self.box = tuple(int(c) for c in box)
        self.gx, self.gy = int(gravity[0]), int(gravity[1])
        self.x, self.y, self.vx, self.vy, self.r = [], [], [], [], []
        self.t = 0
        self.tape = Tape()
        self.contacts_resolved = 0

    # -- construction ----------------------------------------------------------

    def add_disc(self, x, y, vx, vy, r):
        self.x.append(int(x))
        self.y.append(int(y))
        self.vx.append(int(vx))
        self.vy.append(int(vy))
        self.r.append(int(r))
        return len(self.x) - 1

    @classmethod
    def from_units(cls, box, gravity=(0.0, 0.0)):
        """Build a world from world-unit floats. The state stays integer."""
        return cls(tuple(fx(c) for c in box), (fx(gravity[0]), fx(gravity[1])))

    def add_disc_units(self, x, y, vx, vy, r):
        return self.add_disc(fx(x), fx(y), fx(vx), fx(vy), fx(r))

    def __len__(self):
        return len(self.x)

    # -- state -----------------------------------------------------------------

    def state(self):
        """The complete mutable state, as a tuple of ints. Used for exact compares."""
        return (self.t, tuple(self.x), tuple(self.y), tuple(self.vx), tuple(self.vy))

    def set_state(self, st):
        self.t, x, y, vx, vy = st
        self.x, self.y, self.vx, self.vy = list(x), list(y), list(vx), list(vy)

    def momentum(self):
        """Total momentum, assuming equal unit masses. Contact conserves it exactly."""
        return (sum(self.vx), sum(self.vy))

    def kinetic_energy(self):
        """Sum of v^2 in sub-units squared. Integer, so comparisons are exact."""
        return sum(vx * vx + vy * vy for vx, vy in zip(self.vx, self.vy))

    def bounds(self, i):
        x0, y0, x1, y1 = self.box
        r = self.r[i]
        return x0 + r, x1 - r, y0 + r, y1 - r

    def inside(self):
        """True when every centre is within its own wall bounds."""
        for i in range(len(self.x)):
            lox, hix, loy, hiy = self.bounds(i)
            if not (lox <= self.x[i] <= hix and loy <= self.y[i] <= hiy):
                return False
        return True

    # -- the step --------------------------------------------------------------

    def step(self):
        self._kick(1)
        self._drift(1)
        self._contacts(1)
        self.t += 1

    def unstep(self):
        self._contacts(-1)
        self._drift(-1)
        self._kick(-1)
        self.t -= 1

    def run(self, n):
        for _ in range(n):
            self.step()

    def unrun(self, n):
        for _ in range(n):
            self.unstep()

    def _kick(self, sign):
        gx, gy = self.gx * sign, self.gy * sign
        if gx:
            self.vx = [v + gx for v in self.vx]
        if gy:
            self.vy = [v + gy for v in self.vy]

    def _drift(self, sign):
        move = drift_axis if sign > 0 else undrift_axis
        for i in range(len(self.x)):
            lox, hix, loy, hiy = self.bounds(i)
            self.x[i], self.vx[i] = move(self.x[i], self.vx[i], lox, hix)
            self.y[i], self.vy[i] = move(self.y[i], self.vy[i], loy, hiy)

    # -- contact ---------------------------------------------------------------

    def overlapping_pairs(self):
        """Pairs of discs whose centres are closer than the sum of their radii.

        Depends only on positions, which contact resolution does not change. That is
        the property that makes the backward pass find the same pairs as the forward
        pass without recording them.
        """
        pairs = []
        n = len(self.x)
        for i in range(n):
            xi, yi, ri = self.x[i], self.y[i], self.r[i]
            for j in range(i + 1, n):
                dx = xi - self.x[j]
                dy = yi - self.y[j]
                reach = ri + self.r[j]
                if dx * dx + dy * dy < reach * reach:
                    pairs.append((i, j))
        return pairs

    def _contacts(self, sign):
        pairs = self.overlapping_pairs()
        if sign > 0:
            for i, j in pairs:
                self._resolve(i, j)
        else:
            for i, j in reversed(pairs):
                self._unresolve(i, j)

    def _normal(self, i, j):
        dx = self.x[i] - self.x[j]
        dy = self.y[i] - self.y[j]
        return dx, dy, dx * dx + dy * dy

    def _impulse(self, a, dx, dy, d2):
        """Integer impulse for a relative normal speed ``a``. Floor division."""
        return (a * dx) // d2, (a * dy) // d2

    def _resolve(self, i, j):
        """Elastic equal-mass exchange along the line of centres.

        In exact arithmetic this is an involution: applying it twice is the identity,
        because it reflects the relative velocity in the plane normal to the line of
        centres. In integers the floor division makes it *almost* an involution, and
        the gap is exactly one integer, ``k = a + a'``: the relative normal speed
        before the exchange plus the relative normal speed after. In exact arithmetic
        ``a' = -a`` and ``k`` would always be zero. ``k`` is what goes on the tape.
        """
        dx, dy, d2 = self._normal(i, j)
        if d2 == 0:
            # Coincident centres: no line of centres, so no exchange is defined.
            # Skipping is symmetric -- the backward pass sees the same d2 == 0 and
            # also skips -- so reversibility holds.
            return
        a = (self.vx[i] - self.vx[j]) * dx + (self.vy[i] - self.vy[j]) * dy
        jx, jy = self._impulse(a, dx, dy, d2)
        self.vx[i] -= jx
        self.vy[i] -= jy
        self.vx[j] += jx
        self.vy[j] += jy
        a_after = (self.vx[i] - self.vx[j]) * dx + (self.vy[i] - self.vy[j]) * dy
        self.tape.push(a + a_after)
        self.contacts_resolved += 1

    def _unresolve(self, i, j):
        dx, dy, d2 = self._normal(i, j)
        if d2 == 0:
            return
        k = self.tape.pop()
        a_after = (self.vx[i] - self.vx[j]) * dx + (self.vy[i] - self.vy[j]) * dy
        a = k - a_after
        jx, jy = self._impulse(a, dx, dy, d2)
        self.vx[i] += jx
        self.vy[i] += jy
        self.vx[j] -= jx
        self.vy[j] -= jy
        self.contacts_resolved += 1

    # -- reporting -------------------------------------------------------------

    def snapshot_bytes_per_frame(self):
        """Bytes a snapshot-based rewind would store per frame, for comparison.

        Four varint-encoded integers per body -- the same encoding used to measure
        the tape, so the two numbers are comparable.
        """
        return sum(
            varint_len(self.x[i])
            + varint_len(self.y[i])
            + varint_len(self.vx[i])
            + varint_len(self.vy[i])
            for i in range(len(self.x))
        )

    def copy(self):
        w = World(self.box, (self.gx, self.gy))
        w.x, w.y = list(self.x), list(self.y)
        w.vx, w.vy = list(self.vx), list(self.vy)
        w.r = list(self.r)
        w.t = self.t
        w.tape.items = list(self.tape.items)
        return w


__all__ = ["World", "Tape", "TooFast", "TapeError", "drift_axis", "undrift_axis", "SCALE"]
