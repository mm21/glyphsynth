from __future__ import annotations

from ._container import BaseContainer
from ._draw import DrawContainer
from ._export import ExportContainer


class GraphicsContainer(DrawContainer, ExportContainer, BaseContainer):
    pass
