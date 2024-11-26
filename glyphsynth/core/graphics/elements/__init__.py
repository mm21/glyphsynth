"""
Exports classes which encapsulate an SVG element.
"""

from pyrollup import rollup

from . import base, containers, gradients, shapes
from .base import *  # noqa
from .containers import *  # noqa
from .gradients import *  # noqa
from .shapes import *  # noqa

__all__ = rollup(base, containers, shapes, gradients)
