"""Fixed-point helpers.

Every quantity in the simulation is a Python ``int`` counting *sub-units*. There is
no floating point anywhere in the state or in the step, which is what makes a step a
bijection: integer addition, subtraction, negation and floor division by a known
divisor are all exactly invertible, and float rounding is not.

``SCALE`` sub-units make one world unit. 16 bits of fraction is enough that the
half-sub-unit offset used by the wall rule (see ``world.drift_axis``) is 1/131072 of
a world unit.
"""

SCALE = 1 << 16


def fx(value):
    """World units (int or float) -> sub-units."""
    return int(round(value * SCALE))


def unfx(value):
    """Sub-units -> world units, as a float. For rendering and reporting only."""
    return value / SCALE


def zigzag(n):
    """Map a signed int to an unsigned one, small values staying small."""
    return (n << 1) if n >= 0 else ((-n << 1) - 1)


def varint_len(n):
    """Bytes a zigzag varint encoding of ``n`` would take.

    Used to measure the residue tape honestly: the tape's cost is the cost of
    serialising it, not the size of Python's objects.
    """
    z = zigzag(n)
    if z == 0:
        return 1
    return (z.bit_length() + 6) // 7
