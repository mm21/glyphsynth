"""
Alphabet modeled after traditional Latin:
https://en.wikipedia.org/wiki/Latin_alphabet#/media/File:Abecedarium_latinum_clasicum.svg
"""

import sys

from ...letter import LETTERS, BaseLetterGlyph, BaseLetterParams
from ...utils import extend_line

__all__ = [
    "TraditionalLetterParams",
    "LETTER_CLASSES",
    *LETTERS,
]


class TraditionalLetterParams(BaseLetterParams):
    pass


class BaseTraditionalLetterGlyph(BaseLetterGlyph[TraditionalLetterParams]):
    def init(self):
        super().init()
        self.properties.stroke_linejoin = "miter"


class A(BaseTraditionalLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                extend_line(
                    self.inset_top_center,
                    (self.stroke_half, self.canonical_height),
                ),
                self.inset_top_center,
                extend_line(
                    self.inset_top_center,
                    (
                        self.canonical_width - self.stroke_half,
                        self.canonical_height,
                    ),
                ),
            ]
        )

        self.draw_polyline(
            [
                (self.canonical_width / 4, self.canonical_height / 2),
                (self.canonical_width * 3 / 4, self.canonical_height / 2),
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
        # vertical line
        self.draw_polyline(
            [(self.stroke_half, 0.0), (self.stroke_half, self.canonical_height)]
        )
        # top horizontal line
        self.draw_polyline(
            [(0.0, self.stroke_half), (self.canonical_width, self.stroke_half)]
        )
        # middle horizontal line
        self.draw_polyline(
            [
                (0.0, self.canonical_height / 2),
                (self.canonical_width, self.canonical_height / 2),
            ]
        )


class G(BaseLetterGlyph):
    def draw(self):
        ...


class H(BaseLetterGlyph):
    def draw(self):
        ...


class I(BaseLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                (self.canonical_width / 2, 0.0),
                (self.canonical_width / 2, self.canonical_height),
            ]
        )


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
                (self.stroke_half, self.canonical_height),
                (self.stroke_half, 0.0),
                (self.canonical_width / 2, self.canonical_height),
                (self.canonical_width - self.stroke_half, 0.0),
                (
                    self.canonical_width - self.stroke_half,
                    self.canonical_height,
                ),
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
                (self.canonical_width / 2, 0.0),
                (self.canonical_width / 2, self.canonical_height),
            ]
        )

        self.draw_polyline(
            [
                (0.0, self.stroke_half),
                (self.canonical_width, self.stroke_half),
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


LETTER_CLASSES: list[type[BaseLetterGlyph]] = [
    getattr(sys.modules[__name__], l) for l in LETTERS
]
"""
List of letter classes in order.
"""
