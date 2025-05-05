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


class B(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class C(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class D(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class E(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class F(BaseTraditionalLetterGlyph):
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


class G(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class H(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class I(BaseTraditionalLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                (self.canonical_width / 2, 0.0),
                (self.canonical_width / 2, self.canonical_height),
            ]
        )


class J(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class K(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class L(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class M(BaseTraditionalLetterGlyph):
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


class N(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class O(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class P(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class Q(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class R(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class S(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class T(BaseTraditionalLetterGlyph):
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


class U(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class V(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class W(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class X(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class Y(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


class Z(BaseTraditionalLetterGlyph):
    def draw(self):
        ...


LETTER_CLASSES: list[type[BaseLetterGlyph]] = [
    getattr(sys.modules[__name__], l) for l in LETTERS
]
"""
List of letter classes in order.
"""
