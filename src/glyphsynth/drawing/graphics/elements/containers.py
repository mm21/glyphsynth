from __future__ import annotations

from typing import TYPE_CHECKING

import svgwrite.base
import svgwrite.container
import svgwrite.masking
import svgwrite.pattern

from ._factory import ElementFactory
from ._mixins import MaskingMixin, PresentationMixin, TransformMixin, ViewBoxMixin
from .base import BaseElement

if TYPE_CHECKING:
    from ...drawing import BaseDrawing

__all__ = [
    "BaseContainer",
    "Group",
    "Symbol",
    "Marker",
    "Pattern",
    "ClipPath",
    "Mask",
    "Use",
    "ImportedSvg",
]


class BaseContainer[ElementT: svgwrite.base.BaseElement](
    BaseElement[ElementT], ElementFactory
):
    """
    Element which can hold other elements, created using its draw APIs.
    """

    @property
    def _glyph(self) -> BaseDrawing:
        return self._glyph_obj

    @property
    def _container(self) -> ElementT:
        return self._element


class Group(
    BaseContainer[svgwrite.container.Group],
    TransformMixin,
    PresentationMixin,
    MaskingMixin,
):
    """
    Wraps a `<g>` element.
    """

    _api_name = "g"


class Symbol(
    BaseContainer[svgwrite.container.Symbol],
    ViewBoxMixin,
    PresentationMixin,
):
    """
    Wraps a `<symbol>` element: a template which is not rendered directly, but
    instantiated by {obj}`Use` elements.
    """

    _api_name = "symbol"


class Marker(
    BaseContainer[svgwrite.container.Marker],
    ViewBoxMixin,
    PresentationMixin,
):
    """
    Wraps a `<marker>` element: graphics drawn at the vertices of a line, polyline,
    polygon, or path. Apply using `markers()`.
    """

    _api_name = "marker"


class Pattern(
    BaseContainer[svgwrite.pattern.Pattern],
    ViewBoxMixin,
    TransformMixin,
):
    """
    Wraps a `<pattern>` element: a tiled paint server. Apply using `fill(pattern=...)`
    or `stroke(pattern=...)`.
    """

    _api_name = "pattern"

    def get_paint_server(self) -> str:
        return self._element.get_paint_server()


class ClipPath(BaseContainer[svgwrite.masking.ClipPath], TransformMixin):
    """
    Wraps a `<clipPath>` element. Apply using `clip_path()`.
    """

    _api_name = "clipPath"


class Mask(BaseContainer[svgwrite.masking.Mask]):
    """
    Wraps a `<mask>` element, using the luminance of its contents as an alpha mask.
    Apply using `mask()`.
    """

    _api_name = "mask"


class Use(
    BaseElement[svgwrite.container.Use],
    TransformMixin,
    PresentationMixin,
    MaskingMixin,
):
    """
    Wraps a `<use>` element: an instance of another element, such as a {obj}`Symbol`.
    """

    _api_name = "use"


class ImportedSvg(Group):
    """
    Wraps a `<g>` holding the contents of an externally-provided SVG, with its outermost
    `<svg>` element stripped. Created using {obj}`ElementFactory.load_svg`.

    Since the contents are in a group, they can be manipulated together using the
    group's transform and presentation APIs.
    """

    size: tuple[float, float] | None = None
    """
    Size of the original SVG in user units, from its `width`/`height` or `viewBox`;
    `None` if it could not be determined.
    """

    original_viewbox: tuple[float, float, float, float] | None = None
    """
    Original `viewBox` as `(min_x, min_y, width, height)`, if any.
    """

    @property
    def center(self) -> tuple[float, float]:
        """
        Center of the original SVG, in the coordinates in which this group is
        transformed.

        :raises ValueError: If the SVG's size could not be determined
        """
        if self.size is None:
            raise ValueError("SVG does not have a size")
        return (self.size[0] / 2, self.size[1] / 2)

    @property
    def _mixin_size(self) -> tuple[float, float] | None:
        # default center of rotation
        return self.size
