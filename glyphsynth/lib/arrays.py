from abc import ABC
from typing import Sequence

from ..core import BaseGlyph, BaseParams

__all__ = [
    "ArrayParams",
    "HArrayGlyph",
    "VArrayGlyph",
]


class ArrayParams(BaseParams):
    glyphs: Sequence[BaseGlyph]
    spacing: float = 10.0
    center: bool = False


class BaseArrayGlyph(BaseGlyph[ArrayParams], ABC):
    """
    Glyph encapsulating an array of glyphs with constant spacing between them,
    either horizontal or vertical.

    Horizontal arrays grow to the right, and vertical arrays grow downwards.

    If `center` is `True`, glyphs are center aligned.
    """

    _vertical: bool = False

    @classmethod
    def new(
        cls,
        glyphs: Sequence[BaseGlyph],
        glyph_id: str | None = None,
        spacing: float = 0.0,
        center: bool = False,
    ):
        params = cls.params_cls(glyphs=glyphs, spacing=spacing, center=center)
        return cls(params=params, glyph_id=glyph_id)

    def init(self):
        self.size_canon = self._get_size()

    def draw(self):
        # set initial insert point
        insert: tuple[float, float] = (0.0, 0.0)

        for glyph in self.params.glyphs:
            # adjust insert point for this glyph
            insert = self._align_insert(insert, glyph)

            # insert glyph
            self.insert_glyph(glyph, insert)

            # advance insert point
            insert = self._advance_insert(insert, glyph)

    @property
    def _x_center(self) -> float:
        assert self.size_canon is not None
        return self.size_canon[0] / 2

    @property
    def _y_center(self) -> float:
        assert self.size_canon is not None
        return self.size_canon[1] / 2

    def _get_size(self) -> tuple[float, float]:
        width: float
        height: float

        if self._vertical:
            # width: widest glyph
            # height: sum of heights and spacings
            width = max(g.width for g in self.params.glyphs)
            height = self._get_size_dim(1)
        else:
            # width: sum of widths and spacings
            # height: tallest glyph
            width = self._get_size_dim(0)
            height = max(g.height for g in self.params.glyphs)

        return (width, height)

    def _get_size_dim(self, dim: int) -> float:
        """
        Get size along provided dimension. Assumes the array is oriented along
        the provided dimension (e.g. 0 for horizontal).
        """

        length: float = 0.0

        for glyph in self.params.glyphs:
            length += glyph.size[dim]

        # add spacing for all except one
        length += self.params.spacing * (len(self.params.glyphs) - 1)

        return length

    def _align_insert(
        self, insert: tuple[float, float], glyph: BaseGlyph
    ) -> tuple[float, float]:
        """
        Center this glyph to the starting point in the direction of the
        array.
        """

        x: float
        y: float

        if self.params.center:
            # compute one axis of this insertion relative to start, centering
            # the glyph along the appropriate axis
            if self._vertical:
                # align x relative to start, preserve y
                x = self._x_center - (glyph.size[0] / 2)
                y = insert[1]
            else:
                # align y relative to start, preserve x
                x = insert[0]
                y = self._y_center - (glyph.size[1] / 2)
        else:
            # no need to center, just align along the needed dimension
            if self._vertical:
                x = 0.0
                y = insert[1]
            else:
                x = insert[0]
                y = 0.0

        return (x, y)

    def _advance_insert(
        self, insert: tuple[float, float], glyph: BaseGlyph
    ) -> tuple[float, float]:
        if self._vertical:
            # preserve x, advance y
            return (insert[0], insert[1] + glyph.size[1] + self.params.spacing)
        else:
            # preserve y, advance x
            return (insert[0] + glyph.size[0] + self.params.spacing, insert[1])


class HArrayGlyph(BaseArrayGlyph):
    _vertical = False


class VArrayGlyph(BaseArrayGlyph):
    _vertical = True
