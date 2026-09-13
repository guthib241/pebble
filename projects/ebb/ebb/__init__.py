"""ebb — a 2D physics simulation that runs backwards bit-for-bit, with no stored frames."""

from .fixed import SCALE, fx, unfx
from .world import World, Tape, TooFast, TapeError, drift_axis, undrift_axis

__all__ = ["World", "Tape", "TooFast", "TapeError", "drift_axis", "undrift_axis",
           "SCALE", "fx", "unfx"]
__version__ = "0.1.0"
