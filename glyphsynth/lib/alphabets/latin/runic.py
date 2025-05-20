import sys

from ....glyph.glyph import Glyph
from ....glyph.letters import LETTERS

__all__ = [
    "LETTER_CLASSES",
    *LETTERS,
]


class BaseRunicGlyph(Glyph):
    def init(self):
        super().init()
        self.properties.stroke_linejoin = "round"
        self.properties.stroke_linecap = "round"


class A(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_bot,
                self.inset_center_top,
                self.inset_right_bot,
            ]
        )
        self.draw_line(
            (self.inset_quarter_width(1), self.inset_quarter_height(2)),
            (self.inset_quarter_width(3), self.inset_quarter_height(2)),
        )


class B(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline([self.inset_left_top, self.inset_left_bot])
        self.draw_polyline(
            [
                self.inset_left_top,
                (self.inset_right, self.inset_quarter_height(1)),
                self.inset_left_center,
                (self.inset_right, self.inset_quarter_height(3)),
                self.inset_left_bot,
            ]
        )


class C(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_right_top,
                self.inset_left_center,
                self.inset_right_bot,
            ]
        )


class D(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_top,
                self.inset_right_center,
                self.inset_left_bot,
                self.inset_left_top,
            ]
        )


class E(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_right_top,
                self.inset_left_top,
                self.inset_left_bot,
                self.inset_right_bot,
            ]
        )
        self.draw_line(
            self.inset_left_center,
            self.inset_right_center,
        )


class F(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_right_top,
                self.inset_left_top,
                self.inset_left_bot,
            ]
        )
        self.draw_line(
            self.inset_left_center,
            self.inset_right_center,
        )


class G(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                (self.inset_right, self.inset_quarter_height(1)),
                self.inset_center_top,
                (self.inset_left, self.inset_quarter_height(1)),
                # self.inset_left_center,
                (self.inset_left, self.inset_quarter_height(3)),
                self.inset_center_bot,
                (self.inset_right, self.inset_quarter_height(3)),
                self.inset_right_center,
                self.canonical_center,
            ]
        )


class H(BaseRunicGlyph):
    def draw(self):
        self.draw_line(
            self.inset_left_top,
            self.inset_left_bot,
        )
        self.draw_line(
            self.inset_right_top,
            self.inset_right_bot,
        )
        self.draw_line(
            self.inset_left_center,
            self.inset_right_center,
        )


class I(BaseRunicGlyph):
    def draw(self):
        self.draw_line(
            self.inset_center_top,
            self.inset_center_bot,
        )


class J(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_right_top,
                (self.inset_right, self.inset_quarter_height(3)),
                self.inset_center_bot,
                (self.inset_left, self.inset_quarter_height(3)),
            ]
        )


class K(BaseRunicGlyph):
    def draw(self):
        self.draw_line(
            self.inset_left_top,
            self.inset_left_bot,
        )
        self.draw_polyline(
            [
                self.inset_right_top,
                self.inset_left_center,
                self.inset_right_bot,
            ]
        )


class L(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_top,
                self.inset_left_bot,
                self.inset_right_bot,
            ]
        )


class M(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_bot,
                self.inset_left_top,
                self.inset_center_bot,
                self.inset_right_top,
                self.inset_right_bot,
            ]
        )


class N(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_bot,
                self.inset_left_top,
                self.inset_right_bot,
                self.inset_right_top,
            ]
        )


class O(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_center_top,
                self.inset_right_center,
                self.inset_center_bot,
                self.inset_left_center,
                self.inset_center_top,
            ]
        )


class P(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_bot,
                self.inset_left_top,
                (self.inset_right, self.inset_quarter_height(1)),
                self.inset_left_center,
            ]
        )


class Q(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_center_top,
                self.inset_right_center,
                self.inset_center_bot,
                self.inset_left_center,
                self.inset_center_top,
            ]
        )
        self.draw_line(
            self.canonical_center,
            self.inset_right_bot,
        )


class R(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_bot,
                self.inset_left_top,
                (self.inset_right, self.inset_quarter_height(1)),
                self.inset_left_center,
                self.inset_right_bot,
            ]
        )


class S(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                (self.inset_right, self.inset_quarter_height(1)),
                self.inset_center_top,
                (self.inset_left, self.inset_quarter_height(1)),
                (self.inset_right, self.inset_quarter_height(3)),
                self.inset_center_bot,
                (self.inset_left, self.inset_quarter_height(3)),
            ]
        )

        # possible variant
        # self.draw_polyline(
        #    [
        #        self.inset_right_top,
        #        (self.inset_left, self.inset_quarter_height(1)),
        #        (self.inset_right, self.inset_quarter_height(3)),
        #        self.inset_left_bot,
        #    ]
        # )


class T(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_center_top,
                self.inset_center_bot,
            ]
        )
        self.draw_polyline(
            [
                self.inset_left_top,
                self.inset_right_top,
            ]
        )


class U(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_top,
                (self.inset_left, self.inset_quarter_height(3)),
                self.inset_center_bot,
                (self.inset_right, self.inset_quarter_height(3)),
                self.inset_right_top,
            ]
        )


class V(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_top,
                self.inset_center_bot,
                self.inset_right_top,
            ]
        )


class W(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_top,
                (self.inset_quarter_width(1), self.inset_bot),
                self.inset_center_top,
                (self.inset_quarter_width(3), self.inset_bot),
                self.inset_right_top,
            ]
        )


class X(BaseRunicGlyph):
    def draw(self):
        self.draw_line(
            self.inset_left_top,
            self.inset_right_bot,
        )
        self.draw_line(
            self.inset_right_top,
            self.inset_left_bot,
        )


class Y(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_top,
                self.canonical_center,
                self.inset_right_top,
            ]
        )
        self.draw_line(
            self.canonical_center,
            self.inset_center_bot,
        )


class Z(BaseRunicGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_top,
                self.inset_right_top,
                self.inset_left_bot,
                self.inset_right_bot,
            ]
        )


LETTER_CLASSES: list[type[BaseRunicGlyph]] = [
    getattr(sys.modules[__name__], l) for l in LETTERS
]
"""
List of letter classes in order.
"""
