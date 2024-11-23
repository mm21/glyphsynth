from __future__ import annotations

from ._container import BaseContainer
from ._draw import DrawContainer, TransformContainer
from ._export import ExportContainer


class GraphicsContainer(
    DrawContainer, TransformContainer, ExportContainer, BaseContainer
):
    pass
