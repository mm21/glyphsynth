from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING

import svgwrite.base

from ..._utils import normalize_str
from ..properties import ShapeProperties
from .base import BaseElement
from .gradients import LinearGradient, RadialGradient
from .shapes import Circle, Ellipse, Line, Polygon, Polyline, Rect

if TYPE_CHECKING:
    from .base import BaseGlyph
    from .containers import Group

__all__ = [
    "ElementFactory",
]


class ElementFactory(ABC):
    @property
    @abstractmethod
    def _glyph(self) -> BaseGlyph:
        ...

    @property
    @abstractmethod
    def _container(self) -> svgwrite.base.BaseElement:
        ...

    def draw_line(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        properties: ShapeProperties | None = None,
    ) -> Line:
        return Line(
            self._glyph,
            self._container,
            start=start,
            end=end,
            **self._get_extra(properties),
        )

    def draw_polyline(
        self,
        points: Iterable[tuple[float, float]],
        properties: ShapeProperties | None = None,
    ) -> Polyline:
        return Polyline(
            self._glyph,
            self._container,
            points=[p for p in points],
            **self._get_extra(properties),
        )

    def draw_polygon(
        self,
        points: Iterable[tuple[float, float]],
        properties: ShapeProperties | None = None,
    ) -> Polygon:
        return Polygon(
            self._glyph,
            self._container,
            points=[p for p in points],
            **self._get_extra(properties),
        )

    def draw_rect(
        self,
        insert: tuple[float, float],
        size: tuple[float, float],
        radius_x: float | None = None,
        radius_y: float | None = None,
        properties: ShapeProperties | None = None,
    ) -> Rect:
        return Rect(
            self._glyph,
            self._container,
            insert=insert,
            size=size,
            rx=radius_x,
            ry=radius_y,
            **self._get_extra(properties),
        )

    def draw_circle(
        self,
        center: tuple[float, float],
        radius: float,
        properties: ShapeProperties | None = None,
    ) -> Circle:
        return Circle(
            self._glyph,
            self._container,
            center=center,
            r=radius,
            **self._get_extra(properties),
        )

    def draw_ellipse(
        self,
        center: tuple[float, float],
        radius: tuple[float, float],
        properties: ShapeProperties | None = None,
    ) -> Ellipse:
        return Ellipse(
            self._glyph,
            self._container,
            center=center,
            r=radius,
            **self._get_extra(properties),
        )

    def create_group(self, properties: ShapeProperties | None = None) -> Group:
        from .containers import Group

        # only use passed properties instead of inheriting from glyph
        extra = properties._get_values() if properties else {}

        return Group(self._glyph, self._container, **extra)

    def create_linear_gradient(
        self,
        start: tuple[float, float] | None = None,
        end: tuple[float, float] | None = None,
        inherit: str | BaseElement | None = None,
        colors: list[str] | None = None,
        sweep_pct: tuple[float] = (0.0, 100.0),
        opacity: float | int | None = None,
    ) -> LinearGradient:
        elem = LinearGradient(
            self._glyph,
            self._glyph._svg.defs,
            start=start,
            end=end,
            inherit=_normalize_inherit(inherit),
            gradientUnits="userSpaceOnUse",
        )

        if colors:
            elem._element.add_colors(
                colors,
                sweep=[s / 100 for s in sweep_pct],
                opacity=normalize_str(opacity),
            )

        return elem

    def create_radial_gradient(
        self,
        center: tuple[float, float] | None = None,
        radius: float | None = None,
        focal: tuple[float, float] | None = None,
        inherit: str | BaseElement | None = None,
        colors: list[str] | None = None,
        sweep_pct: tuple[float] = (0.0, 100.0),
        opacity: float | int | None = None,
    ) -> RadialGradient:
        elem = RadialGradient(
            self._glyph,
            self._glyph._svg.defs,
            center=center,
            r=radius,
            focal=focal,
            inherit=_normalize_inherit(inherit),
            gradientUnits="userSpaceOnUse",
        )

        if colors:
            elem._element.add_colors(
                colors,
                sweep=[s / 100 for s in sweep_pct],
                opacity=normalize_str(opacity),
            )

        return elem

    def _get_extra(self, properties: ShapeProperties | None) -> dict[str, str]:
        """
        Get extra kwargs to pass to svgwrite APIs.
        """
        # override defaults from the glyph with given properties
        props = ShapeProperties._aggregate(
            self._glyph.properties,
            properties,
        )
        return props._get_values()


def _normalize_inherit(inherit: str | BaseElement | None) -> str | None:
    if isinstance(inherit, BaseElement):
        return inherit.iri
