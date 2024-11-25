from __future__ import annotations

from collections.abc import Iterable

from .._utils import normalize_str
from ._container import BaseContainer
from .elements.base import BaseElement
from .elements.container import Group
from .elements.gradients import LinearGradient, RadialGradient
from .elements.shapes import Circle, Ellipse, Line, Polygon, Polyline, Rect
from .properties import ShapeProperties


def _normalize_inherit(inherit: str | BaseElement | None) -> str | None:
    if isinstance(inherit, BaseElement):
        return inherit.iri


# TODO: move to mixins as BaseDrawMixin
# - define property: _mixin_container, returns self._svg
# - also use for Group
class DrawContainer(BaseContainer):
    def draw_line(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        properties: ShapeProperties | None = None,
    ) -> Line:
        return Line(
            self._drawing,
            self._svg,
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
            self._drawing,
            self._svg,
            points=[p for p in points],
            **self._get_extra(properties),
        )

    def draw_polygon(
        self,
        points: Iterable[tuple[float, float]],
        properties: ShapeProperties | None = None,
    ) -> Polygon:
        return Polygon(
            self._drawing,
            self._svg,
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
            self._drawing,
            self._svg,
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
            self._drawing,
            self._svg,
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
            self._drawing,
            self._svg,
            center=center,
            r=radius,
            **self._get_extra(properties),
        )

    def create_group(self, properties: ShapeProperties | None = None) -> Group:
        return Group(self._drawing, self._svg, **self._get_extra(properties))

    def create_linear_gradient(
        self,
        start: tuple[float, float] | None = None,
        end: tuple[float, float] | None = None,
        inherit: str | BaseElement | None = None,
        colors: list[str] | None = None,
        sweep_pct: tuple[float] = (0.0, 100.0),
        opacity: float | None = None,
    ) -> LinearGradient:
        elem = LinearGradient(
            self._drawing,
            self._drawing.defs,
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
        opacity: float | None = None,
    ) -> RadialGradient:
        elem = RadialGradient(
            self._drawing,
            self._drawing.defs,
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
        # aggregate provided properties with those of the glyph
        props = ShapeProperties._aggregate(
            [self.properties] + ([properties] if properties else [])
        )
        return props._get_values()
