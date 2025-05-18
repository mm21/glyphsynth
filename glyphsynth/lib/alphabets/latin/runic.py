import sys

from ...letter import LETTERS, BaseLetterGlyph, BaseLetterParams

__all__ = [
    "RunicLetterParams",
    "LETTER_CLASSES",
    *LETTERS,
]


class RunicLetterParams(BaseLetterParams):
    pass


class BaseRunicLetterGlyph(BaseLetterGlyph[RunicLetterParams]):
    def init(self):
        super().init()
        self.properties.stroke_linejoin = "round"
        self.properties.stroke_linecap = "round"


class A(BaseRunicLetterGlyph):
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


class B(BaseRunicLetterGlyph):
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


class C(BaseRunicLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_right_top,
                self.inset_left_center,
                self.inset_right_bot,
            ]
        )


class D(BaseRunicLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_top,
                self.inset_right_center,
                self.inset_left_bot,
                self.inset_left_top,
            ]
        )


class E(BaseRunicLetterGlyph):
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


class F(BaseRunicLetterGlyph):
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


class G(BaseRunicLetterGlyph):
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


class H(BaseRunicLetterGlyph):
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


class I(BaseRunicLetterGlyph):
    def draw(self):
        self.draw_line(
            self.inset_center_top,
            self.inset_center_bot,
        )


class J(BaseRunicLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_right_top,
                (self.inset_right, self.inset_quarter_height(3)),
                self.inset_center_bot,
                (self.inset_left, self.inset_quarter_height(3)),
            ]
        )


class K(BaseRunicLetterGlyph):
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


class L(BaseRunicLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_top,
                self.inset_left_bot,
                self.inset_right_bot,
            ]
        )


class M(BaseRunicLetterGlyph):
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


class N(BaseRunicLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_bot,
                self.inset_left_top,
                self.inset_right_bot,
                self.inset_right_top,
            ]
        )


class O(BaseRunicLetterGlyph):
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


class P(BaseRunicLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_bot,
                self.inset_left_top,
                (self.inset_right, self.inset_quarter_height(1)),
                self.inset_left_center,
            ]
        )


class Q(BaseRunicLetterGlyph):
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


class R(BaseRunicLetterGlyph):
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


class S(BaseRunicLetterGlyph):
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


class T(BaseRunicLetterGlyph):
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


class U(BaseRunicLetterGlyph):
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


class V(BaseRunicLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_top,
                self.inset_center_bot,
                self.inset_right_top,
            ]
        )


class W(BaseRunicLetterGlyph):
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


class X(BaseRunicLetterGlyph):
    def draw(self):
        self.draw_line(
            self.inset_left_top,
            self.inset_right_bot,
        )
        self.draw_line(
            self.inset_right_top,
            self.inset_left_bot,
        )


class Y(BaseRunicLetterGlyph):
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


class Z(BaseRunicLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_top,
                self.inset_right_top,
                self.inset_left_bot,
                self.inset_right_bot,
            ]
        )


LETTER_CLASSES: list[type[BaseLetterGlyph]] = [
    getattr(sys.modules[__name__], l) for l in LETTERS
]
"""
List of letter classes in order.
"""
