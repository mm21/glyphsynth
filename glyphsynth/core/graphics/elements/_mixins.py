"""
Mixins to provide APIs.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Self

import svgwrite.mixins

from ..._utils import normalize_str

if TYPE_CHECKING:
    from .gradients import BaseGradient

__all__ = [
    "ViewBoxMixin",
    "TransformMixin",
    "PresentationMixin",
    "MarkersMixin",
]


def _normalize_color(
    color: str | None, gradient: BaseGradient | None
) -> str | None:
    return (
        color
        if color is not None
        else gradient.funciri
        if gradient is not None
        else None
    )


class BaseWrapperMixin[T]:
    """
    Wraps an svgwrite mixin.
    """

    _mixin_obj: T


class ViewBoxMixin(BaseWrapperMixin[svgwrite.mixins.ViewBox]):
    def viewbox(
        self, min_x: float, min_y: float, width: float, height: float
    ) -> Self:
        self._mixin_obj.viewbox(min_x, min_y, width, height)
        return self

    def stretch(self) -> Self:
        self._mixin_obj.stretch()
        return self

    def fit(
        self,
        horiz: Literal["left", "center", "right"] = "center",
        vert: Literal["top", "middle", "bottom"] = "middle",
        scale: Literal["meet", "slice"] = "meet",
    ) -> Self:
        self._mixin_obj.fit(horiz=horiz, vert=vert, scale=scale)
        return self


class TransformMixin(BaseWrapperMixin[svgwrite.mixins.Transform]):
    def translate(self, x: float, y: float | None = None) -> Self:
        self._mixin_obj.translate(x, y)
        return self

    def rotate(
        self, angle: float, center: tuple[float, float] | None = None
    ) -> Self:
        # set center if none was provided and we have a size
        if center is None:
            if (size := self._mixin_size) is not None:
                center = (size[0] / 2, size[1] / 2)

        self._mixin_obj.rotate(angle, center=center)
        return self

    def scale(self, x: float, y: float | None = None) -> Self:
        self._mixin_obj.scale(x, y)
        return self

    def skew_x(self, angle: float) -> Self:
        self._mixin_obj.skewX(angle)
        return self

    def skew_y(self, angle: float) -> Self:
        self._mixin_obj.skewY(angle)
        return self

    def matrix(
        self,
        scale_x: float,
        scale_y: float,
        skew_x: float,
        skew_y: float,
        translate_x: float,
        translate_y: float,
    ) -> Self:
        self._mixin_obj.matrix(
            scale_x, scale_y, skew_x, skew_y, translate_x, translate_y
        )
        return self

    @property
    def _mixin_size(self) -> tuple[float, float] | None:
        """
        Overridden by subclass if applicable.
        """
        return None


class PresentationMixin(BaseWrapperMixin[svgwrite.mixins.Presentation]):
    def fill(
        self,
        color: str | None = None,
        gradient: BaseGradient | None = None,
        rule: str | None = None,
        opacity_pct: float | int | None = None,
    ) -> Self:
        self._mixin_obj.fill(
            color=_normalize_color(color, gradient),
            rule=rule,
            opacity=normalize_str(
                opacity_pct / 100 if opacity_pct is not None else None
            ),
        )
        return self

    def stroke(
        self,
        color: str | None,
        gradient: BaseGradient | None = None,
        width: float | None = None,
        opacity_pct: float | int | None = None,
        linecap: Literal["butt", "round", "square"] | None = None,
        linejoin: Literal["arcs", "bevel", "miter", "miter-clip", "round"]
        | None = None,
        miterlimit: int | float | None = None,
    ) -> Self:
        self._mixin_obj.stroke(
            color=_normalize_color(color, gradient),
            width=normalize_str(width),
            opacity=normalize_str(
                opacity_pct / 100 if opacity_pct is not None else None
            ),
            linecap=normalize_str(linecap),
            linejoin=normalize_str(linejoin),
            miterlimit=normalize_str(miterlimit),
        )
        return self

    def dasharray(
        self,
        dasharray: list[int | float] | None = None,
        offset: float | str | None = None,
    ) -> Self:
        self._mixin_obj.dasharray(
            dasharray=dasharray, offset=normalize_str(offset)
        )
        return self


class MarkersMixin(BaseWrapperMixin[svgwrite.mixins.Markers]):
    pass


# may not be necessary
"""
class ClippingMixin(BaseWrapperMixin[svgwrite.mixins.Clipping]):
    pass
"""
