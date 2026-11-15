"""
Path element, supporting lines, curves, and arcs.
"""

from __future__ import annotations

import math
from typing import Self

import svgwrite.path

from ._mixins import MarkersMixin, MaskingMixin, PresentationMixin, TransformMixin
from .base import BaseElement

__all__ = [
    "Path",
]

type _Point = tuple[float | int, float | int]
type _Radius = float | int | tuple[float | int, float | int]

_PRECISION = 10
"""
Number of decimal places to round computed coordinates to, avoiding output such as
`6.123233995736766e-15` for values which are effectively zero.
"""


class Path(
    BaseElement[svgwrite.path.Path],
    TransformMixin,
    PresentationMixin,
    MarkersMixin,
    MaskingMixin,
):
    """
    Wraps a `<path>` element. Commands are appended using chainable methods, e.g.:

    ```python
    path = drawing.draw_path().move_to((0, 0)).line_to((10, 0)).arc_to(
        (10, 10), radius=5
    ).close()
    ```

    All commands take absolute coordinates unless `relative=True` is passed.
    """

    _api_name = "path"

    def move_to(self, point: _Point, relative: bool = False) -> Self:
        """
        Start a new subpath at the given point.
        """
        return self._push("M", relative, *point)

    def line_to(self, point: _Point, relative: bool = False) -> Self:
        """
        Draw a straight line to the given point.
        """
        return self._push("L", relative, *point)

    def horizontal_to(self, x: float | int, relative: bool = False) -> Self:
        """
        Draw a horizontal line to the given x-coordinate.
        """
        return self._push("H", relative, x)

    def vertical_to(self, y: float | int, relative: bool = False) -> Self:
        """
        Draw a vertical line to the given y-coordinate.
        """
        return self._push("V", relative, y)

    def cubic_to(
        self,
        control1: _Point,
        control2: _Point,
        end: _Point,
        relative: bool = False,
    ) -> Self:
        """
        Draw a cubic Bézier curve to `end` using the given control points.
        """
        return self._push("C", relative, *control1, *control2, *end)

    def smooth_cubic_to(
        self, control2: _Point, end: _Point, relative: bool = False
    ) -> Self:
        """
        Draw a cubic Bézier curve to `end`, with the first control point being the
        reflection of the previous command's second control point.
        """
        return self._push("S", relative, *control2, *end)

    def quadratic_to(
        self, control: _Point, end: _Point, relative: bool = False
    ) -> Self:
        """
        Draw a quadratic Bézier curve to `end` using the given control point.
        """
        return self._push("Q", relative, *control, *end)

    def smooth_quadratic_to(self, end: _Point, relative: bool = False) -> Self:
        """
        Draw a quadratic Bézier curve to `end`, with the control point being the
        reflection of the previous command's control point.
        """
        return self._push("T", relative, *end)

    def arc_to(
        self,
        end: _Point,
        radius: _Radius,
        rotation: float | int = 0,
        large_arc: bool = False,
        sweep: bool = True,
        relative: bool = False,
    ) -> Self:
        """
        Draw an elliptical arc to `end`.

        :param end: End point of arc
        :param radius: Radius as a single value for a circular arc, or `(rx, ry)`
        :param rotation: Rotation of the ellipse's x-axis in degrees
        :param large_arc: Whether to choose the arc spanning 180 degrees or more
        :param sweep: Whether to draw the arc in the direction of increasing angle,
            i.e. clockwise in SVG's y-down coordinate system
        :param relative: Whether `end` is relative to the current point
        """
        rx, ry = _normalize_radius(radius)
        return self._push(
            "A", relative, rx, ry, rotation, int(large_arc), int(sweep), *end
        )

    def arc(
        self,
        center: _Point,
        radius: _Radius,
        start_angle: float | int,
        end_angle: float | int,
        connect: bool = True,
    ) -> Self:
        """
        Draw an arc of a circle or axis-aligned ellipse specified by its center and
        angles. Angles are in degrees, measured clockwise from the positive x-axis; the
        arc is drawn clockwise if `end_angle > start_angle` and counterclockwise
        otherwise. A span of 360 degrees or more draws a full circle/ellipse.

        :param center: Center of the circle/ellipse
        :param radius: Radius as a single value for a circular arc, or `(rx, ry)`
        :param start_angle: Start angle in degrees
        :param end_angle: End angle in degrees
        :param connect: Whether to draw a line from the current point to the start
            of the arc; if `False` or there is no current point, a new subpath is
            started at the start of the arc
        """
        rx, ry = _normalize_radius(radius)
        span = end_angle - start_angle
        sweep = span >= 0

        start = _get_ellipse_point(center, (rx, ry), start_angle)
        end = _get_ellipse_point(center, (rx, ry), end_angle)

        # svgwrite seeds commands with None when no initial data is given
        if connect and any(c is not None for c in self._element.commands):
            self.line_to(start)
        else:
            self.move_to(start)

        if abs(span) >= 360:
            # a single arc can't have coincident endpoints: split into two halves
            mid = _get_ellipse_point(
                center, (rx, ry), start_angle + math.copysign(180, span)
            )
            self.arc_to(mid, (rx, ry), sweep=sweep)
            self.arc_to(start, (rx, ry), sweep=sweep)
        else:
            self.arc_to(end, (rx, ry), large_arc=abs(span) > 180, sweep=sweep)

        return self

    def close(self) -> Self:
        """
        Close the current subpath by drawing a line to its start.
        """
        self._element.push("Z")
        return self

    def push(self, *commands: str | float | int) -> Self:
        """
        Push raw path commands and coordinates, e.g. `push("M", 0, 0, "L", 10, 10)`.
        """
        self._element.push(*commands)
        return self

    def _push(self, command: str, relative: bool, *args: float | int) -> Self:
        self._element.push(command.lower() if relative else command, *args)
        return self


def _normalize_radius(radius: _Radius) -> tuple[float | int, float | int]:
    return (radius, radius) if isinstance(radius, (float, int)) else radius


def _get_ellipse_point(
    center: _Point, radius: tuple[float | int, float | int], angle: float | int
) -> tuple[float, float]:
    theta = math.radians(angle)
    return (
        round(center[0] + radius[0] * math.cos(theta), _PRECISION) + 0.0,
        round(center[1] + radius[1] * math.sin(theta), _PRECISION) + 0.0,
    )
