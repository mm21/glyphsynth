import string
import sys

from pydantic import Field

from ....core.glyph import BaseGlyph, BaseParams
from ....core.graphics import Properties
from ...utils import extend_line

LETTERS_STR = string.ascii_uppercase
"""
Assume there are classes in this module with single-letter names A-Z.
"""

__all__ = [
    "LetterParams",
    "BaseLetterGlyph",
    "LetterComboParams",
    "BaseLetterComboGlyph",
    "ZERO",
    "UNIT",
    "HALF",
    "LETTER_CLS_LIST",
    *LETTERS_STR,
]

ZERO = 0.0
UNIT = 100.0
HALF = UNIT / 2
QUART = HALF / 2


class LetterParams(BaseParams):
    color: str = "black"
    stroke_pct: float = 5.0


class BaseLetterGlyph(BaseGlyph[LetterParams]):
    size_canon = (UNIT, UNIT)

    default_properties = Properties(
        fill="none",
        stroke="black",
        stroke_linejoin="bevel",
    )

    _stroke_width: float

    def init(self):
        self._stroke_width = (self.params.stroke_pct / 100) * UNIT
        self.properties.stroke_width = str(round(self._stroke_width))
        self.properties.stroke = self.params.color

    @property
    def _stroke_half(self) -> float:
        return self._stroke_width / 2

    @property
    def _stroke_start(self) -> float:
        return self._stroke_half

    @property
    def _stroke_end(self) -> float:
        return UNIT - self._stroke_half


class LetterComboParams(BaseParams):
    """
    Contains parameters to propagate to letters.
    """

    letter_params: LetterParams = Field(default_factory=LetterParams)


class BaseLetterComboGlyph[ParamsT: LetterComboParams](BaseGlyph[ParamsT]):
    """
    Glyph which encapsulates a combination of overlayed letter glyphs.
    """

    size_canon = (UNIT, UNIT)

    def draw_letter[
        LetterT: BaseLetterGlyph
    ](self, letter_cls: type[LetterT]) -> LetterT:
        return letter_cls(parent=self, params=self.params.letter_params)

    def draw_combo[
        ComboT: BaseLetterComboGlyph
    ](self, combo_cls: type[ComboT]) -> ComboT:
        return combo_cls(parent=self, params=self.params)


class A(BaseLetterGlyph):
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


class B(BaseLetterGlyph):
    def draw(self):
        ...


class C(BaseLetterGlyph):
    def draw(self):
        ...


class D(BaseLetterGlyph):
    def draw(self):
        ...


class E(BaseLetterGlyph):
    def draw(self):
        ...


class F(BaseLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [(self._stroke_half, ZERO), (self._stroke_half, UNIT)]
        )
        self.draw_polyline(
            [(ZERO, self._stroke_half), (UNIT, self._stroke_half)]
        )
        self.draw_polyline([(ZERO, HALF), (UNIT, HALF)])


class G(BaseLetterGlyph):
    def draw(self):
        ...


class H(BaseLetterGlyph):
    def draw(self):
        ...


class I(BaseLetterGlyph):
    def draw(self):
        self.draw_polyline([(HALF, ZERO), (HALF, UNIT)])


class J(BaseLetterGlyph):
    def draw(self):
        ...


class K(BaseLetterGlyph):
    def draw(self):
        ...


class L(BaseLetterGlyph):
    def draw(self):
        ...


class M(BaseLetterGlyph):
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


class N(BaseLetterGlyph):
    def draw(self):
        ...


class O(BaseLetterGlyph):
    def draw(self):
        ...


class P(BaseLetterGlyph):
    def draw(self):
        ...


class Q(BaseLetterGlyph):
    def draw(self):
        ...


class R(BaseLetterGlyph):
    def draw(self):
        ...


class S(BaseLetterGlyph):
    def draw(self):
        ...


class T(BaseLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                (ZERO, self._stroke_start),
                (UNIT, self._stroke_start),
                (HALF, self._stroke_start),
                (HALF, UNIT),
            ]
        )


class U(BaseLetterGlyph):
    def draw(self):
        ...


class V(BaseLetterGlyph):
    def draw(self):
        ...


class W(BaseLetterGlyph):
    def draw(self):
        ...


class X(BaseLetterGlyph):
    def draw(self):
        ...


class Y(BaseLetterGlyph):
    def draw(self):
        ...


class Z(BaseLetterGlyph):
    def draw(self):
        ...


LETTER_CLS_LIST: list[type[BaseLetterGlyph]] = [
    getattr(sys.modules[__name__], l) for l in LETTERS_STR
]
"""
List of letter classes in order.
"""
