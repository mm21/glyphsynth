"""
Image element.
"""

from __future__ import annotations

from typing import Literal, Self

import svgwrite.image

from ._mixins import MaskingMixin, TransformMixin
from .base import BaseElement

__all__ = [
    "Image",
]


class Image(BaseElement[svgwrite.image.Image], TransformMixin, MaskingMixin):
    """
    Wraps an `<image>` element referencing an external or embedded (data URI) raster or
    SVG image.
    """

    _api_name = "image"

    def stretch(self) -> Self:
        """
        Stretch image to fill its viewport, ignoring aspect ratio.
        """
        self._element.stretch()
        return self

    def fit(
        self,
        horiz: Literal["left", "center", "right"] = "center",
        vert: Literal["top", "middle", "bottom"] = "middle",
        scale: Literal["meet", "slice"] = "meet",
    ) -> Self:
        """
        Fit image to its viewport, preserving aspect ratio.
        """
        self._element.fit(horiz=horiz, vert=vert, scale=scale)
        return self
