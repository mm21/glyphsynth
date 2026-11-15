"""
Mixins to provide APIs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Self, cast

import svgwrite.base
import svgwrite.mixins

from ..._utils import normalize_str

if TYPE_CHECKING:
    from .base import BaseElement
    from .containers import ClipPath, Marker, Mask, Pattern
    from .gradients import BaseGradient

__all__ = [
    "ViewBoxMixin",
    "TransformMixin",
    "PresentationMixin",
    "MarkersMixin",
    "MaskingMixin",
]


class BaseWrapperMixin[T]:
    """
    Wraps an svgwrite mixin.
    """

    _mixin_obj: T


class ViewBoxMixin[T: svgwrite.mixins.ViewBox](BaseWrapperMixin[T]):
    def viewbox(self, min_x: float, min_y: float, width: float, height: float) -> Self:
        # svgwrite stubs declare int, but floats are valid
        self._mixin_obj.viewbox(
            min_x, min_y, width, height  # pyright: ignore[reportArgumentType]
        )
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


class TransformMixin[T: svgwrite.mixins.Transform](BaseWrapperMixin[T]):
    def translate(self, x: float | int, y: float | int | None = None) -> Self:
        self._mixin_obj.translate(x, y)
        return self

    def rotate(
        self,
        angle: float | int,
        center: tuple[float | int, float | int] | None = None,
    ) -> Self:
        # set center if none was provided and we have a size
        if center is None:
            if (size := self._mixin_size) is not None:
                center = (size[0] / 2, size[1] / 2)

        self._mixin_obj.rotate(angle, center=center)
        return self

    def scale(self, x: float | int, y: float | int | None = None) -> Self:
        self._mixin_obj.scale(x, y)
        return self

    def skew_x(self, angle: float | int) -> Self:
        self._mixin_obj.skewX(angle)
        return self

    def skew_y(self, angle: float | int) -> Self:
        self._mixin_obj.skewY(angle)
        return self

    def matrix(
        self,
        scale_x: float | int,
        scale_y: float | int,
        skew_x: float | int,
        skew_y: float | int,
        translate_x: float | int,
        translate_y: float | int,
    ) -> Self:
        self._mixin_obj.matrix(
            scale_x, scale_y, skew_x, skew_y, translate_x, translate_y
        )
        return self

    # TODO: flip(): scale to create mirror image across given axes

    @property
    def _mixin_size(self) -> tuple[float, float] | None:
        """
        Overridden by subclass if applicable.
        """
        return None


class PresentationMixin[T: svgwrite.mixins.Presentation](BaseWrapperMixin[T]):
    def fill(
        self,
        color: str | None = None,
        gradient: BaseGradient | None = None,
        rule: str | None = None,
        opacity_pct: float | int | None = None,
        pattern: Pattern | None = None,
    ) -> Self:
        self._mixin_obj.fill(
            color=_normalize_color(color, gradient, pattern),
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
        linejoin: (
            Literal["arcs", "bevel", "miter", "miter-clip", "round"] | None
        ) = None,
        miterlimit: int | float | None = None,
        pattern: Pattern | None = None,
    ) -> Self:
        self._mixin_obj.stroke(
            color=_normalize_color(color, gradient, pattern),
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
        self._mixin_obj.dasharray(dasharray=dasharray, offset=normalize_str(offset))
        return self


class MarkersMixin[T: svgwrite.mixins.Markers](BaseWrapperMixin[T]):
    def markers(
        self,
        start: Marker | str | None = None,
        mid: Marker | str | None = None,
        end: Marker | str | None = None,
    ) -> Self:
        """
        Set markers drawn at the start, interior vertices, and end of this shape.
        Markers may be given as {obj}`Marker` objects or IRI strings (`"#id"`).
        """
        element = cast(svgwrite.base.BaseElement, self._mixin_obj)
        for attr, marker in (
            ("marker-start", start),
            ("marker-mid", mid),
            ("marker-end", end),
        ):
            if marker is not None:
                element[attr] = _get_funciri(marker)
        return self


class MaskingMixin[T: svgwrite.base.BaseElement](BaseWrapperMixin[T]):
    def clip_path(self, clip_path: ClipPath | str) -> Self:
        """
        Restrict painting of this element to the region of the given clip path.
        """
        self._mixin_obj["clip-path"] = _get_funciri(clip_path)
        return self

    def mask(self, mask: Mask | str) -> Self:
        """
        Composite this element using the given mask.
        """
        self._mixin_obj["mask"] = _get_funciri(mask)
        return self


def _get_funciri(element: BaseElement | str) -> str:
    """
    Get FuncIRI (`url(#id)`) of an element or IRI string (`#id`).
    """
    return f"url({element})" if isinstance(element, str) else element.funciri


def _normalize_color(
    color: str | None,
    gradient: BaseGradient | None,
    pattern: Pattern | None = None,
) -> str | None:
    if color is not None:
        return color
    if gradient is not None:
        return gradient.funciri
    if pattern is not None:
        return pattern.funciri
    return None
