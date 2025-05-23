import os

from pyrollup import rollup

from . import elements, properties
from .elements import *  # noqa
from .properties import *  # noqa

__all__ = ["RASTER_SUPPORT"] + rollup(elements, properties)

RASTER_SUPPORT: bool = os.name == "posix"
"""
Whether rasterization is supported; Linux only.
"""
