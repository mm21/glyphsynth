import svgwrite.shapes

from ._mixins import MarkersMixin, MaskingMixin, PresentationMixin, TransformMixin
from .base import BaseElement

__all__ = [
    "Line",
    "Rect",
    "Circle",
    "Ellipse",
    "Polyline",
    "Polygon",
]


class Line(
    BaseElement[svgwrite.shapes.Line],
    TransformMixin,
    PresentationMixin,
    MarkersMixin,
    MaskingMixin,
):
    _api_name = "line"


class Rect(
    BaseElement[svgwrite.shapes.Rect],
    TransformMixin,
    PresentationMixin,
    MaskingMixin,
):
    _api_name = "rect"


class Circle(
    BaseElement[svgwrite.shapes.Circle],
    TransformMixin,
    PresentationMixin,
    MaskingMixin,
):
    _api_name = "circle"


class Ellipse(
    BaseElement[svgwrite.shapes.Ellipse],
    TransformMixin,
    PresentationMixin,
    MaskingMixin,
):
    _api_name = "ellipse"


class Polyline(
    BaseElement[svgwrite.shapes.Polyline],
    TransformMixin,
    PresentationMixin,
    MarkersMixin,
    MaskingMixin,
):
    _api_name = "polyline"


class Polygon(
    BaseElement[svgwrite.shapes.Polygon],
    TransformMixin,
    PresentationMixin,
    MarkersMixin,
    MaskingMixin,
):
    _api_name = "polygon"
