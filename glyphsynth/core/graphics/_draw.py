from __future__ import annotations

from collections.abc import Iterable
from typing import Self, cast

from svgwrite.container import Group

from svgwrite.shapes import (
    Line,
    Rect,
    Circle,
    Ellipse,
    Polyline,
    Polygon,
)

from ._container import BaseContainer
from .properties import (
    Properties,
    BasePropertiesModel,
    PaintingPropertiesMixin,
    ShapeProperties,
)


class DrawContainer(BaseContainer):
    def draw_line(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        properties: ShapeProperties | None = None,
    ) -> Line:
        elem: Line = self._drawing.line(
            start=start,
            end=end,
            **self._get_extra(properties),
        )

        self._svg.add(elem)

        return elem

    def draw_polyline(
        self,
        points: Iterable[tuple[float, float]],
        properties: ShapeProperties | None = None,
    ) -> Polyline:
        elem: Polyline = self._drawing.polyline(
            points=[p for p in points],
            **self._get_extra(properties),
        )

        self._svg.add(elem)

        return elem

    def draw_polygon(
        self,
        points: Iterable[tuple[float, float]],
        properties: ShapeProperties | None = None,
    ) -> Polygon:
        elem: Polygon = self._drawing.polygon(
            points=[p for p in points],
            **self._get_extra(properties),
        )

        self._svg.add(elem)

        return elem

    def draw_rect(
        self,
        insert: tuple[float, float],
        size: tuple[float, float],
        radius_x: float | None = None,
        radius_y: float | None = None,
        properties: ShapeProperties | None = None,
    ) -> Rect:
        elem: Rect = self._drawing.rect(
            insert=insert,
            size=size,
            rx=radius_x,
            ry=radius_y,
            **self._get_extra(properties),
        )

        self._svg.add(elem)

        return elem

    def draw_circle(
        self,
        center: tuple[float, float],
        radius: float,
        properties: ShapeProperties | None = None,
    ) -> Circle:
        elem: Circle = self._drawing.circle(
            center=center, r=radius, **self._get_extra(properties)
        )

        self._svg.add(elem)

        return elem

    def draw_ellipse(
        self,
        center: tuple[float, float],
        radius: tuple[float, float],
        properties: ShapeProperties | None = None,
    ) -> Ellipse:
        elem: Ellipse = self._drawing.ellipse(
            center=center, r=radius, **self._get_extra(properties)
        )

        self._svg.add(elem)

        return elem

    def draw_group(self, properties: ShapeProperties | None = None) -> Group:
        elem: Group = self._drawing.g(**self._get_extra(properties))

        self._svg.add(elem)

        return elem

    def _get_extra(self, properties: ShapeProperties | None) -> dict[str, str]:
        """
        Get extra kwargs to pass to svgwrite APIs.
        """

        # aggregate provided properties with those of the glyph
        all_props = tuple(
            [self.properties]
            if properties is None
            else [self.properties, properties]
        )
        props = ShapeProperties._aggregate(
            [self.properties] + ([properties] if properties else [])
        )

        return props._get_values()


# TODO: other methods of https://svgwrite.readthedocs.io/en/latest/classes/mixins.html#svgwrite.mixins.Transform
class TransformContainer(BaseContainer):
    def rotate(
        self, angle: float, center: tuple[float, float] | None = None
    ) -> Self:
        # set center if none was provided and we have a size
        if center is None and self.size is not None:
            center = (self.size[0] / 2, self.size[1] / 2)

        self._group.rotate(angle, center=center)

        return self

    def scale(self, x: float, y: float | None = None) -> Self:
        if y is None:
            y = x

        self._group.scale(x, y)

        return self
