"""orbiter: flags Python code that mixes units, like milliseconds passed as seconds."""

from __future__ import annotations

__version__ = "0.1.0"

from .analyze import AnalysisError, Diagnostic, analyze_paths
from .config import CODES, Config, load_config

__all__ = [
    "AnalysisError",
    "CODES",
    "Config",
    "Diagnostic",
    "analyze_paths",
    "load_config",
    "__version__",
]
