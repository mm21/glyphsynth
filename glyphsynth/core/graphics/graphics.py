from __future__ import annotations

from .draw import DrawContainer, TransformContainer
from .export import ExportContainer
from .container import BaseContainer

__all__ = []


class GraphicsContainer(
    DrawContainer, TransformContainer, ExportContainer, BaseContainer
):
    pass
