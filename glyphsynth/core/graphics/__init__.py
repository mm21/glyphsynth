import os

from pyrollup import rollup

from . import properties
from .properties import *

__all__ = ["RASTER_SUPPORT"] + rollup(properties)

RASTER_SUPPORT: bool = os.name == "posix"
"""
Whether rasterization is supported; Linux only.
"""

# TODO: add types.py?
# - Coordinate
# - Box/Area
