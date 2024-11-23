from pyrollup import rollup

from . import letters
from .letters import *  # noqa

__all__ = rollup(letters)
