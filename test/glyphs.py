from __future__ import annotations

from glyphsynth import BaseDrawing, BaseParams, Properties, ShapeProperties
from glyphsynth.core.graphics.elements.shapes import Circle

__all__ = ["BasicDrawing", "ParentDrawing", "ParentDrawing2"]

ZERO = 0.0
ORIGIN = (ZERO, ZERO)
UNIT = 100.0
HALF = UNIT / 2
CENTER = (HALF, HALF)
SIZE = (UNIT, UNIT)

BASIC_STROKE_PCT: float = 5.0
BASIC_STROKE_WIDTH: float = BASIC_STROKE_PCT * UNIT / 100
BASIC_STROKE_HALF: float = BASIC_STROKE_WIDTH / 2


class BasicParams(BaseParams):
    color1: str = "black"
    color2: str = "blue"


class BasicDrawing(BaseDrawing[BasicParams]):
    canonical_size = (UNIT, UNIT)

    default_properties = Properties(
        stroke_width=BASIC_STROKE_WIDTH,
        stroke_linecap="round",
        stroke_linejoin="round",
    )

    def init(self):
        self.properties.stroke = self.params.color1

    def draw(self):
        # add a little extra to avoid slight clipping on boundaries
        inset = (self.properties.stroke_width / 2) + 0.1

        self.draw_polyline([(inset, inset), (UNIT - inset, UNIT - inset)])
        self.draw_polyline(
            [(HALF, inset), (UNIT - inset, HALF)],
            properties=Properties(stroke=self.params.color2),
        )


class ParentDrawing(BaseDrawing):
    child1: BasicDrawing
    child2: BasicDrawing

    canonical_size = BasicDrawing.canonical_size

    def draw(self):
        params2: BasicParams = BasicParams(color1="red")

        self.child1 = self.insert_drawing(
            BasicDrawing(size=self.canonical_size)
        )
        self.child2 = self.insert_drawing(
            BasicDrawing(size=self.canonical_size, params=params2)
        )

        # rotate child2
        self.child2.rotate(90.0)

        assert self.child2.params.color1 == "red"
        assert self.child2.params.color2 == "blue"


class ParentDrawing2(ParentDrawing):
    def init(self):
        assert BasicDrawing.canonical_size is not None
        self.canonical_size = (
            BasicDrawing.canonical_size[0] * 10,
            BasicDrawing.canonical_size[1] * 10,
        )


class GradientDrawing(BaseDrawing):
    canonical_size = (UNIT, UNIT)

    circle: Circle

    def draw(self):
        self.draw_rect(ORIGIN, SIZE, properties=ShapeProperties(fill="black"))

        gradient = self.create_radial_gradient(
            center=CENTER,
            radius=HALF,
            colors=["red", "blue"],
        )
        self.circle = self.draw_circle(CENTER, HALF)
        self.circle.fill(gradient=gradient)
