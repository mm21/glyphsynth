from __future__ import annotations

from glyphsynth import (
    BaseGlyph,
    BaseParams,
    Properties,
    PropertyValueType,
    ShapeProperties,
)
from glyphsynth.core.graphics.elements.shapes import Circle
from glyphsynth.lib.alphabet.minimal import UNIT, ZERO

__all__ = ["BasicGlyph", "ParentGlyph", "ParentGlyph2"]

BASIC_STROKE_PCT: float = 5.0
BASIC_STROKE_WIDTH: float = BASIC_STROKE_PCT * UNIT / 100
BASIC_STROKE_HALF: float = BASIC_STROKE_WIDTH / 2


class BasicParams(BaseParams):
    color1: str = "black"


class BasicGlyph(BaseGlyph[BasicParams]):
    class DefaultProperties(Properties):
        stroke: PropertyValueType = "black"
        stroke_width: PropertyValueType = str(BASIC_STROKE_WIDTH)

    size_canon = (UNIT, UNIT)

    def init(self):
        self.properties.color = self.params.color1
        self.properties.stroke = self.params.color1

    def draw(self):
        self.draw_polyline([(ZERO, ZERO), (UNIT, UNIT)])


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


class ParentGlyph2(ParentGlyph):
    def init(self):
        assert BasicGlyph.size_canon is not None
        self.size_canon = (
            BasicGlyph.size_canon[0] * 10,
            BasicGlyph.size_canon[1] * 10,
        )


ORIGIN = (0.0, 0.0)
UNIT = 100.0
HALF = UNIT / 2
CENTER = (HALF, HALF)
SIZE = (UNIT, UNIT)


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
        self.circle = self.draw_circle(
            CENTER, HALF, properties=ShapeProperties(gradient=gradient)
        )
