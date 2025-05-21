"""
Base glyph classes.
"""
from __future__ import annotations

from functools import cached_property

from ..core.drawing import BaseDrawing, BaseParams

__all__ = [
    "GlyphParams",
    "BaseGlyph",
    "Glyph",
]

UNIT = 100.0


class Anchors:
    """
    Encapsulates a set of anchor points within a given window for convenience.
    """

    __glyph: BaseGlyph
    __inset: float

    def __init__(self, glyph: BaseGlyph, inset: float):
        self.__glyph = glyph
        self.__inset = inset

    @property
    def width(self) -> float:
        return self.__glyph.canonical_width - 2 * self.__inset

    @property
    def height(self) -> float:
        return self.__glyph.canonical_height - 2 * self.__inset

    @property
    def top_border(self) -> float:
        return self.__inset

    @property
    def bot_border(self) -> float:
        return self.__glyph.canonical_height - self.__inset

    @property
    def left_border(self) -> float:
        return self.__inset

    @property
    def left_top(self) -> tuple[float, float]:
        return (self.left_border, self.top_border)

    @property
    def left_center(self) -> tuple[float, float]:
        return (self.left_border, self.__glyph.canonical_height / 2)

    @property
    def left_bot(self) -> tuple[float, float]:
        return (self.left_border, self.bot_border)

    @cached_property
    def center_top(self) -> tuple[float, float]:
        return (self.__glyph.canonical_width / 2, self.top_border)

    @cached_property
    def center_bot(self) -> tuple[float, float]:
        return (self.__glyph.canonical_width / 2, self.bot_border)

    @property
    def right_border(self) -> float:
        return self.__glyph.canonical_width - self.__inset

    @cached_property
    def right_top(self) -> tuple[float, float]:
        return (self.right_border, self.top_border)

    @cached_property
    def right_center(self) -> tuple[float, float]:
        return (self.right_border, self.__glyph.canonical_height / 2)

    @cached_property
    def right_bot(self) -> tuple[float, float]:
        return (self.right_border, self.bot_border)

    def quarter_width(self, ordinal: int) -> float:
        """
        Get width at the provided quarter interval.
        """
        return self.left_border + self.width * (ordinal / 4)

    def quarter_height(self, ordinal: int) -> float:
        """
        Get height at the provided quarter interval.
        """
        return self.top_border + self.height * (ordinal / 4)


class GlyphParams(BaseParams):
    """
    Common glyph parameters.
    """

    color: str = "black"
    stroke_pct: float = 5.0
    aspect_ratio: tuple[int, int] = (3, 5)

    @property
    def stroke_width(self) -> float:
        return UNIT * self.stroke_pct / 100

    @property
    def stroke_half(self) -> float:
        return self.stroke_width / 2


class BaseGlyph[ParamsT: GlyphParams](BaseDrawing[ParamsT]):
    """
    Base glyph class to be subclassed by user.
    """

    stroke_offset: bool = True
    """
    Whether to add an offset to the size to account for stroke width. Enables
    consistent ratios for stroked lines regardless of stroke width.
    """

    __border_anchors: Anchors
    __inset_anchors: Anchors

    @property
    def nominal_size(self) -> tuple[float, float]:
        """
        Size used to place points, accounting for any inset based on stroke
        width.
        """
        return (
            self.canonical_size[0] - self._size_offset,
            self.canonical_size[1] - self._size_offset,
        )

    @property
    def border(self) -> Anchors:
        """
        Anchors based on the overall border of the glyph.
        """
        return self.__border_anchors

    @property
    def inset(self) -> Anchors:
        """
        Anchors based on the stroke width such that stroked lines exactly meet
        the overall border.
        """
        return self.__inset_anchors

    def init(self):
        self.properties.fill = "none"
        self.properties.stroke = self.params.color
        self.properties.stroke_width = str(round(self.params.stroke_width, 2))

        # set canonical_size based on aspect ratio
        aspect_ratio_x, aspect_ratio_y = self.params.aspect_ratio

        if aspect_ratio_x < aspect_ratio_y:
            width_scaled = UNIT * (aspect_ratio_x / aspect_ratio_y)
            height_scaled = UNIT
        else:
            width_scaled = UNIT
            height_scaled = UNIT * (aspect_ratio_y / aspect_ratio_x)

        self.canonical_size = (
            width_scaled + self._size_offset,
            height_scaled + self._size_offset,
        )

    def draw_glyph[
        GlyphT: BaseGlyph
    ](
        self,
        glyph_cls: type[GlyphT],
        params: GlyphParams | None = None,
        scale: float | int | None = None,
        preserve_stroke_width: bool = False,
    ) -> GlyphT:
        params_norm = (params or self.params).model_copy()

        nominal_size_x, nominal_size_y = self.nominal_size
        size = (
            (
                nominal_size_x * scale + self._size_offset,
                nominal_size_y * scale + self._size_offset,
            )
            if scale
            else None
        )

        if scale and not preserve_stroke_width:
            # adjust stroke width to match that of parent, accounting for
            # rescaling
            params_norm.stroke_pct = self.params.stroke_pct / scale

        glyph = glyph_cls(params=params_norm, size=size)

        self.insert_drawing(glyph)
        return glyph

    @property
    def _size_offset(self) -> float:
        """
        Offset from perimeter, accounting for stroke width if applicable.
        """
        return 2 * self.params.stroke_width if self.stroke_offset else 0

    def _pre_init(self):
        self.__border_anchors = Anchors(self, 0.0)
        self.__inset_anchors = Anchors(self, self.params.stroke_half)


class Glyph(BaseGlyph[GlyphParams]):
    """
    Empty glyph which uses the base `GlyphParams`.
    """

    def draw(self):
        pass
