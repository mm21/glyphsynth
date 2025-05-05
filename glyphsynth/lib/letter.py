"""
Base letter and letter combination glyphs.
"""

import string
from functools import cached_property

from pydantic import Field

from ..core.glyph import BaseGlyph, BaseParams

__all__ = [
    "BaseLetterParams",
    "BaseLetterGlyph",
]

LETTERS: list[str] = [l for l in string.ascii_uppercase]
"""
List of letters A-Z.
"""

ZERO = 0.0
UNIT = 100.0
HALF = UNIT / 2
QUART = HALF / 2


class BaseLetterParams(BaseParams):
    """
    Common letter parameters.
    """

    color: str = "black"
    stroke_pct: float = 5.0
    aspect_ratio: tuple[int, int] = (3, 5)

    @property
    def stroke_width(self) -> float:
        return UNIT * self.stroke_pct / 100


class BaseLetterGlyph[ParamsT: BaseLetterParams](BaseGlyph[ParamsT]):
    @cached_property
    def stroke_width(self) -> float:
        return self.params.stroke_width

    @cached_property
    def stroke_half(self) -> float:
        return self.stroke_width / 2

    @cached_property
    def top_left(self) -> tuple[float, float]:
        return (0.0, 0.0)

    @cached_property
    def top_center(self) -> tuple[float, float]:
        return (self.canonical_width / 2, 0.0)

    @cached_property
    def top_right(self) -> tuple[float, float]:
        return (self.canonical_width, 0.0)

    @cached_property
    def left_center(self) -> tuple[float, float]:
        return (0.0, self.canonical_height / 2)

    @cached_property
    def right_center(self) -> tuple[float, float]:
        return (self.canonical_width, self.canonical_height / 2)

    @cached_property
    def bot_left(self) -> tuple[float, float]:
        return (0.0, self.canonical_height)

    @cached_property
    def bot_center(self) -> tuple[float, float]:
        return (self.canonical_width / 2, self.canonical_height)

    @cached_property
    def bot_right(self) -> tuple[float, float]:
        return (self.canonical_width, self.canonical_height)

    @cached_property
    def inset_width(self) -> float:
        """
        Width of inset drawing area.
        """
        return UNIT * (
            self.params.aspect_ratio[0] / self.params.aspect_ratio[1]
        )

    @cached_property
    def inset_height(self) -> float:
        """
        Height of inset drawing area.
        """
        return UNIT

    @cached_property
    def inset_top_left(self) -> tuple[float, float]:
        return (self.stroke_half, self.stroke_half)

    @cached_property
    def inset_top_center(self) -> tuple[float, float]:
        return (self.canonical_width / 2, self.stroke_half)

    @cached_property
    def inset_top_right(self) -> tuple[float, float]:
        return (self.canonical_width - self.stroke_half, self.stroke_half)

    @cached_property
    def inset_left_center(self) -> tuple[float, float]:
        return (self.stroke_half, self.canonical_height / 2)

    @cached_property
    def inset_right_center(self) -> tuple[float, float]:
        return (
            self.canonical_width - self.stroke_half,
            self.canonical_height / 2,
        )

    @cached_property
    def inset_bot_left(self) -> tuple[float, float]:
        return (self.stroke_half, self.canonical_height - self.stroke_half)

    @cached_property
    def inset_bot_center(self) -> tuple[float, float]:
        return (
            self.canonical_width / 2,
            self.canonical_height - self.stroke_half,
        )

    @cached_property
    def inset_bot_right(self) -> tuple[float, float]:
        return (
            self.canonical_width - self.stroke_half,
            self.canonical_height - self.stroke_half,
        )

    def init(self):
        self.properties.fill = "none"
        self.properties.stroke = self.params.color
        self.properties.stroke_width = str(round(self.stroke_width, 2))

        self.canonical_size = (
            self.inset_width + self.stroke_width,
            self.inset_height + self.stroke_width,
        )


class LetterComboParams(BaseParams):
    """
    Contains parameters to propagate to letters.
    """

    letter_params: BaseLetterParams = Field(default_factory=BaseLetterParams)


class BaseLetterComboGlyph[ParamsT: LetterComboParams](BaseGlyph[ParamsT]):
    """
    Glyph which encapsulates a combination of overlayed letter glyphs.
    """

    def init(self):
        self.canonical_size = (
            UNIT + self.params.letter_params.stroke_width,
            UNIT + self.params.letter_params.stroke_width,
        )

    def draw_letter[
        LetterT: BaseLetterGlyph
    ](self, letter_cls: type[LetterT]) -> LetterT:
        return self.insert_glyph(letter_cls(params=self.params.letter_params))

    def draw_combo[
        ComboT: BaseLetterComboGlyph
    ](self, combo_cls: type[ComboT]) -> ComboT:
        return self.insert_glyph(combo_cls(params=self.params))
