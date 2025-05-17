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
        self.draw_polyline(
            [
                (self.inset_quarter_width(1), self.inset_quarter_height(2)),
                (self.inset_quarter_width(3), self.inset_quarter_height(2)),
            ]
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
        self.draw_polyline(
            [
                self.inset_left_center,
                self.inset_right_center,
            ]
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
        self.draw_polyline(
            [
                self.inset_left_center,
                self.inset_right_center,
            ]
        )


class G(BaseRunicLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                (self.inset_right, self.inset_quarter_height(1)),
                self.inset_center_top,
                self.inset_left_center,
                self.inset_center_bot,
                (self.inset_right, self.inset_quarter_height(3)),
                self.inset_right_center,
                self.center,
            ]
        )


class H(BaseRunicLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_left_top,
                self.inset_left_bot,
            ]
        )
        self.draw_polyline(
            [
                self.inset_right_top,
                self.inset_right_bot,
            ]
        )
        self.draw_polyline(
            [
                self.inset_left_center,
                self.inset_right_center,
            ]
        )


class I(BaseRunicLetterGlyph):
    def draw(self):
        self.draw_polyline(
            [
                self.inset_center_top,
                self.inset_center_bot,
            ]
        )


class J(BaseRunicLetterGlyph):
    def draw(self):
        ...


class K(BaseRunicLetterGlyph):
    def draw(self):
        ...


class L(BaseRunicLetterGlyph):
    def draw(self):
        ...


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
        ...


class O(BaseRunicLetterGlyph):
    def draw(self):
        ...


class P(BaseRunicLetterGlyph):
    def draw(self):
        ...


class Q(BaseRunicLetterGlyph):
    def draw(self):
        ...


class R(BaseRunicLetterGlyph):
    def draw(self):
        ...


class S(BaseRunicLetterGlyph):
    def draw(self):
        ...


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
        ...


class V(BaseRunicLetterGlyph):
    def draw(self):
        ...


class W(BaseRunicLetterGlyph):
    def draw(self):
        ...


class X(BaseRunicLetterGlyph):
    def draw(self):
        ...


class Y(BaseRunicLetterGlyph):
    def draw(self):
        ...


class Z(BaseRunicLetterGlyph):
    def draw(self):
        ...


LETTER_CLASSES: list[type[BaseLetterGlyph]] = [
    getattr(sys.modules[__name__], l) for l in LETTERS
]
"""
List of letter classes in order.
"""
