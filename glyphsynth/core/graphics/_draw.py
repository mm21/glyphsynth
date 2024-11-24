from __future__ import annotations

from collections.abc import Iterable

from ._container import BaseContainer
from .elements.base import BaseElement
from .elements.container import Group
from .elements.gradients import LinearGradient, RadialGradient
from .elements.shapes import Circle, Ellipse, Line, Polygon, Polyline, Rect
from .properties import ShapeProperties


def _normalize_inherit(inherit: str | BaseElement | None) -> str | None:
    if isinstance(inherit, BaseElement):
        return inherit.get_iri()


class DrawContainer(BaseContainer):
    def draw_line(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        properties: ShapeProperties | None = None,
    ) -> Line:
        elem = Line(
            self._drawing, start=start, end=end, **self._get_extra(properties)
        )
        self._svg.add(elem._element)
        return elem

    def draw_polyline(
        self,
        points: Iterable[tuple[float, float]],
        properties: ShapeProperties | None = None,
    ) -> Polyline:
        elem = Polyline(
            self._drawing,
            points=[p for p in points],
            **self._get_extra(properties),
        )
        self._svg.add(elem._element)
        return elem

    def draw_polygon(
        self,
        points: Iterable[tuple[float, float]],
        properties: ShapeProperties | None = None,
    ) -> Polygon:
        elem = Polygon(
            self._drawing,
            points=[p for p in points],
            **self._get_extra(properties),
        )
        self._svg.add(elem._element)
        return elem

    def draw_rect(
        self,
        insert: tuple[float, float],
        size: tuple[float, float],
        radius_x: float | None = None,
        radius_y: float | None = None,
        properties: ShapeProperties | None = None,
    ) -> Rect:
        elem = Rect(
            self._drawing,
            insert=insert,
            size=size,
            rx=radius_x,
            ry=radius_y,
            **self._get_extra(properties),
        )
        self._svg.add(elem._element)
        return elem

    def draw_circle(
        self,
        center: tuple[float, float],
        radius: float,
        properties: ShapeProperties | None = None,
    ) -> Circle:
        elem = Circle(
            self._drawing,
            center=center,
            r=radius,
            **self._get_extra(properties),
        )
        self._svg.add(elem._element)
        return elem

    def draw_ellipse(
        self,
        center: tuple[float, float],
        radius: tuple[float, float],
        properties: ShapeProperties | None = None,
    ) -> Ellipse:
        elem = Ellipse(
            self._drawing,
            center=center,
            r=radius,
            **self._get_extra(properties),
        )
        self._svg.add(elem._element)
        return elem

    def draw_group(self, properties: ShapeProperties | None = None) -> Group:
        elem = Group(self._drawing, **self._get_extra(properties))
        self._svg.add(elem._element)
        return elem

    def create_linear_gradient(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        inherit: str | BaseElement | None = None,
    ) -> LinearGradient:
        elem = LinearGradient(self._drawing)
        self._svg.add(elem._element)
        return elem

    def create_radial_gradient(self) -> RadialGradient:
        elem = RadialGradient(self._drawing)
        self._svg.add(elem._element)
        return elem

    def _get_extra(self, properties: ShapeProperties | None) -> dict[str, str]:
        """
        Get extra kwargs to pass to svgwrite APIs.
        """
        # aggregate provided properties with those of the glyph
        props = ShapeProperties._aggregate(
            [self.properties] + ([properties] if properties else [])
        )
        return props._get_values()
