from __future__ import annotations

from collections.abc import Iterable
from typing import Self

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
from .properties import BaseProperties, PaintingProperties


class DrawContainer(BaseContainer):
    def draw_line(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        **extra: str,
    ) -> Line:
        elem: Line = self._drawing.line(
            start=start,
            end=end,
            **self._get_extra_painting(extra),
        )

        self._svg.add(elem)

        return elem

    def draw_polyline(
        self,
        points: Iterable[tuple[float, float]],
        **extra: str,
    ) -> Polyline:
        elem: Polyline = self._drawing.polyline(
            points=[p for p in points],
            **self._get_extra_painting(extra),
        )

        self._svg.add(elem)

        return elem

    def draw_polygon(
        self,
        points: Iterable[tuple[float, float]],
        **extra: str,
    ) -> Polygon:
        elem: Polygon = self._drawing.polyline(
            points=[p for p in points],
            **self._get_extra_painting(extra),
        )

        self._svg.add(elem)

        return elem

    def draw_rect(
        self,
        insert: tuple[float, float],
        size: tuple[float, float],
        radius_x: float | None = None,
        radius_y: float | None = None,
        **extra: str,
    ) -> Rect:
        elem: Rect = self._drawing.rect(
            insert=insert,
            size=size,
            rx=radius_x,
            ry=radius_y,
            **self._get_extra_painting(extra),
        )

        self._svg.add(elem)

        return elem

    def draw_circle(
        self,
        center: tuple[float, float],
        radius: float,
        **extra: str,
    ) -> Circle:
        elem: Circle = self._drawing.circle(
            center=center, r=radius, **self._get_extra_painting(extra)
        )

        self._svg.add(elem)

        return elem

    def draw_ellipse(
        self,
        center: tuple[float, float],
        radius: tuple[float, float],
        **extra: str,
    ) -> Ellipse:
        elem: Ellipse = self._drawing.ellipse(
            center=center, r=radius, **self._get_extra_painting(extra)
        )

        self._svg.add(elem)

        return elem

    def draw_group(self, **extra: str) -> Group:
        elem: Group = self._drawing.g(**extra)

        self._svg.add(elem)

        return elem

    def _get_extra(
        self, extra: dict[str, str], *extra_cls: type[BaseProperties]
    ) -> dict[str, str]:
        # get extras defined on each class
        valid_extras = []
        for cls in extra_cls:
            valid_extras += list(cls.model_fields.keys())

        for attr in extra:
            assert attr in valid_extras, f"Invalid extra {attr}"

        ret = extra.copy()

        # check for extra attributes defined on class
        for attr in valid_extras:
            # explicitly provided extra takes precedence
            if attr in extra:
                continue

            if (value := getattr(self.properties, attr)) is not None:
                ret[attr] = value

        return ret

    def _get_extra_painting(self, extra: dict[str, str]) -> dict[str, str]:
        return self._get_extra(extra, PaintingProperties)


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
