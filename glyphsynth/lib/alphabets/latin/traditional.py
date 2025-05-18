"""
Alphabet modeled after traditional Latin:
https://en.wikipedia.org/wiki/Latin_alphabet#/media/File:Abecedarium_latinum_clasicum.svg
"""

import sys

from ....glyph.glyph import BaseGlyph, GlyphParams
from ....glyph.letters import LETTERS
from ...utils import extend_line

__all__ = [
    "LETTER_CLASSES",
    *LETTERS,
]


class BaseTraditionalGlyph(BaseGlyph[GlyphParams]):
    def init(self):
        super().init()
        self.properties.stroke_linejoin = "miter"


class A(BaseTraditionalGlyph):
    def draw(self):
        self.draw_polyline(
            [
                extend_line(
                    self.inset_center_top,
                    (self.stroke_half, self.canonical_height),
                ),
                self.inset_center_top,
                extend_line(
                    self.inset_center_top,
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


class B(BaseTraditionalGlyph):
    def draw(self):
        ...


class C(BaseTraditionalGlyph):
    def draw(self):
        ...


class D(BaseTraditionalGlyph):
    def draw(self):
        ...


class E(BaseTraditionalGlyph):
    def draw(self):
        ...


class F(BaseTraditionalGlyph):
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


class G(BaseTraditionalGlyph):
    def draw(self):
        ...


class H(BaseTraditionalGlyph):
    def draw(self):
        ...


class I(BaseTraditionalGlyph):
    def draw(self):
        self.draw_polyline(
            [
                (self.canonical_width / 2, 0.0),
                (self.canonical_width / 2, self.canonical_height),
            ]
        )


class J(BaseTraditionalGlyph):
    def draw(self):
        ...


class K(BaseTraditionalGlyph):
    def draw(self):
        ...


class L(BaseTraditionalGlyph):
    def draw(self):
        ...


class M(BaseTraditionalGlyph):
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


class N(BaseTraditionalGlyph):
    def draw(self):
        ...


class O(BaseTraditionalGlyph):
    def draw(self):
        ...


class P(BaseTraditionalGlyph):
    def draw(self):
        ...


class Q(BaseTraditionalGlyph):
    def draw(self):
        ...


class R(BaseTraditionalGlyph):
    def draw(self):
        ...


class S(BaseTraditionalGlyph):
    def draw(self):
        ...


class T(BaseTraditionalGlyph):
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


class U(BaseTraditionalGlyph):
    def draw(self):
        ...


class V(BaseTraditionalGlyph):
    def draw(self):
        ...


class W(BaseTraditionalGlyph):
    def draw(self):
        ...


class X(BaseTraditionalGlyph):
    def draw(self):
        ...


class Y(BaseTraditionalGlyph):
    def draw(self):
        ...


class Z(BaseTraditionalGlyph):
    def draw(self):
        ...


LETTER_CLASSES: list[type[BaseTraditionalGlyph]] = [
    getattr(sys.modules[__name__], l) for l in LETTERS
]
"""
List of letter classes in order.
"""
