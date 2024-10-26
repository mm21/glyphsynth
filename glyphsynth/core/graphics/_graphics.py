from __future__ import annotations

from ._draw import DrawContainer, TransformContainer
from ._export import ExportContainer
from ._container import BaseContainer


class GraphicsContainer(
    DrawContainer, TransformContainer, ExportContainer, BaseContainer
):
    pass
