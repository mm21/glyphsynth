"""
Mixins to provide APIs.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Self

import svgwrite.mixins

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
        else gradient.get_funciri()
        if gradient is not None
        else None
    )


def _str(v: Any | None) -> str | None:
    return None if v is None else str(v)


class BaseMixin[T]:
    """
    Wraps an svgwrite mixin.
    """

    _mixin_obj: T


class ViewBoxMixin(BaseMixin[svgwrite.mixins.ViewBox]):
    def viewbox(self, min_x: float, min_y: float, width: float, height: float):
        self._mixin_obj.viewbox(min_x, min_y, width, height)

    def stretch(self):
        self._mixin_obj.stretch()

    def fit(
        self,
        horiz: Literal["left", "center", "right"] = "center",
        vert: Literal["top", "middle", "bottom"] = "middle",
        scale: Literal["meet", "slice"] = "meet",
    ):
        self._mixin_obj.fit(horiz=horiz, vert=vert, scale=scale)


class TransformMixin(BaseMixin[svgwrite.mixins.Transform]):
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


class PresentationMixin(BaseMixin[svgwrite.mixins.Presentation]):
    def fill(
        self,
        color: str | None = None,
        gradient: BaseGradient | None = None,
        rule: str | None = None,
        opacity: float | None = None,
    ):
        self._mixin_obj.fill(
            color=_normalize_color(color, gradient),
            rule=rule,
            opacity=_str(opacity),
        )

    def stroke(
        self,
        color: str | None,
        gradient: BaseGradient | None = None,
        width: float | None = None,
        opacity: float | None = None,
        linecap: Literal["butt", "round", "square"] | None = None,
        linejoin: Literal["arcs", "bevel", "miter", "miter-clip", "round"]
        | None = None,
        miterlimit: int | float | None = None,
    ):
        self._mixin_obj.stroke(
            color=_normalize_color(color, gradient),
            width=_str(width),
            opacity=_str(opacity),
            linecap=_str(linecap),
            linejoin=_str(linejoin),
            miterlimit=_str(miterlimit),
        )

    def dasharray(
        self,
        dasharray: list[int | float] | None = None,
        offset: float | str | None = None,
    ):
        self._mixin_obj.dasharray(dasharray=dasharray, offset=_str(offset))


# TODO
class MarkersMixin(BaseMixin[svgwrite.mixins.Markers]):
    pass


class ClippingMixin(BaseMixin[svgwrite.mixins.Clipping]):
    pass
