"""A simple geospatial greeting package for GISCI 343 live coding.

Three things to demonstrate.

1. ``hello`` shows the absolute minimum function inside a package.
2. ``load_sensors`` shows the bundled-data pattern (data ships in the
   package and is found at runtime with ``importlib.resources``).
3. ``load_sa2_auckland`` shows the fetched-data pattern (data is
   downloaded from the Stats NZ Datafinder WFS endpoint and cached
   locally on first use).
"""

from __future__ import annotations

from .core import hello
from .loader import load_sa2_auckland, load_sensors

__version__ = "0.1.0"

__all__ = [
    "hello",
    "load_sensors",
    "load_sa2_auckland",
]
