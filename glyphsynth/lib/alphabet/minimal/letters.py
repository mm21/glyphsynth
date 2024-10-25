import string

from glyphsynth.core.glyph import BaseGlyph, BaseParams
from glyphsynth.core.graphics import Properties, PropertyValue
from ...utils import extend_line


letters_str = string.ascii_uppercase
"""
Assume there are classes in this module with single-letter names A-Z.
"""

__all__ = [
    "LetterParams",
    "BaseLetter",
    "ZERO",
    "UNIT",
    "HALF",
    "letter_cls_list",
    *letters_str,
]

ZERO = 0.0
UNIT = 100.0
HALF = UNIT / 2
QUART = HALF / 2


class LetterParams(BaseParams):
    stroke_pct: float = 5.0


# TODO:
# - rename: BaseLetterGlyph
class BaseLetter(BaseGlyph[LetterParams]):
    _stroke_width: float

    class DefaultProperties(Properties):
        fill: PropertyValue = "none"
        stroke: PropertyValue = "black"
        stroke_linejoin: PropertyValue = "bevel"

    size_canon = (UNIT, UNIT)

    def init(self):
        self._stroke_width = (self.params.stroke_pct / 100) * UNIT
        self.properties.stroke_width = str(round(self._stroke_width))

    @property
    def _stroke_half(self) -> float:
        return self._stroke_width / 2

    @property
    def _stroke_start(self) -> float:
        return self._stroke_half

    @property
    def _stroke_end(self) -> float:
        return UNIT - self._stroke_half


# TODO: can't use polyline - use individual lines with clipping
# - "polyline" helper
class A(BaseLetter):
    def draw(self):
        # top point
        top = (HALF, ZERO)

        self.draw_polyline(
            [
                extend_line((self._stroke_start, UNIT), top),
                top,
                extend_line((self._stroke_end, UNIT), top),
            ]
        )

        self.draw_polyline(
            [
                (QUART, HALF),
                (QUART * 3, HALF),
            ]
        )


class B(BaseLetter):
    def draw(self):
        ...


class C(BaseLetter):
    def draw(self):
        ...


class D(BaseLetter):
    def draw(self):
        ...


class E(BaseLetter):
    def draw(self):
        ...


class F(BaseLetter):
    def draw(self):
        self.draw_polyline(
            [(self._stroke_half, ZERO), (self._stroke_half, UNIT)]
        )
        self.draw_polyline(
            [(ZERO, self._stroke_half), (UNIT, self._stroke_half)]
        )
        self.draw_polyline([(ZERO, HALF), (UNIT, HALF)])


class G(BaseLetter):
    def draw(self):
        ...


class H(BaseLetter):
    def draw(self):
        ...


class I(BaseLetter):
    def draw(self):
        self.draw_polyline([(HALF, ZERO), (HALF, UNIT)])


class J(BaseLetter):
    def draw(self):
        ...


class K(BaseLetter):
    def draw(self):
        ...


class L(BaseLetter):
    def draw(self):
        ...


class M(BaseLetter):
    def draw(self):
        self.draw_polyline(
            [
                (self._stroke_half, UNIT),
                (self._stroke_half, ZERO),
                (HALF, UNIT),  # TODO: determine ideal y-coordinate
                (self._stroke_end, ZERO),
                (self._stroke_end, UNIT),
            ]
        )


class N(BaseLetter):
    def draw(self):
        ...


class O(BaseLetter):
    def draw(self):
        ...


class P(BaseLetter):
    def draw(self):
        ...


class Q(BaseLetter):
    def draw(self):
        ...


class R(BaseLetter):
    def draw(self):
        ...


class S(BaseLetter):
    def draw(self):
        ...


class T(BaseLetter):
    def draw(self):
        self.draw_polyline(
            [
                (ZERO, self._stroke_start),
                (UNIT, self._stroke_start),
                (HALF, self._stroke_start),
                (HALF, UNIT),
            ]
        )


class U(BaseLetter):
    def draw(self):
        ...


class V(BaseLetter):
    def draw(self):
        ...


class W(BaseLetter):
    def draw(self):
        ...


class X(BaseLetter):
    def draw(self):
        ...


class Y(BaseLetter):
    def draw(self):
        ...


class Z(BaseLetter):
    def draw(self):
        ...


letter_cls_list: list[type[BaseLetter]] = [eval(l) for l in letters_str]
"""
List of letter classes in order.
"""
