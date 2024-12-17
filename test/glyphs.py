from __future__ import annotations

from glyphsynth import BaseGlyph, BaseParams, Properties, ShapeProperties
from glyphsynth.core.graphics.elements.shapes import Circle

__all__ = ["BasicGlyph", "ParentGlyph", "ParentGlyph2"]

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


class BasicGlyph(BaseGlyph[BasicParams]):
    size_canon = (UNIT, UNIT)

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


class ParentGlyph(BaseGlyph):
    child1: BasicGlyph
    child2: BasicGlyph

    size_canon = BasicGlyph.size_canon

    def draw(self):
        params2: BasicParams = BasicParams(color1="red")

        self.child1 = BasicGlyph(size=self.size_canon, parent=self)
        self.child2 = BasicGlyph(
            size=self.size_canon, params=params2, parent=self
        )

        # rotate child2
        self.child2.rotate(90.0)

        assert self.child2.params.color1 == "red"
        assert self.child2.params.color2 == "blue"


class ParentGlyph2(ParentGlyph):
    def init(self):
        assert BasicGlyph.size_canon is not None
        self.size_canon = (
            BasicGlyph.size_canon[0] * 10,
            BasicGlyph.size_canon[1] * 10,
        )


class GradientGlyph(BaseGlyph):
    size_canon = (UNIT, UNIT)

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
