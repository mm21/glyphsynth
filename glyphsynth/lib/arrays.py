from abc import ABC

from ..core import BaseGlyph

__all__ = [
    "HArrayGlyph",
    "VArrayGlyph",
]

from .matrix import BaseMatrixGlyph


class BaseArrayGlyph(BaseMatrixGlyph, ABC):
    """
    Glyph encapsulating an array of glyphs with constant spacing between them,
    either horizontal or vertical.

    Horizontal arrays grow to the right, and vertical arrays grow downwards.

    If `center` is `True`, glyphs are center aligned with respect to the other
    axis. That is, horizontal arrays would be centered vertically and vertical
    arrays would be centered horizontally.
    """

    _horizontal: bool = False

    @classmethod
    def new(
        cls,
        glyphs: list[BaseGlyph],
        glyph_id: str | None = None,
        spacing: float = 0.0,
        padding: float = 0.0,
        center: bool = True,
    ):
        rows = [glyphs] if cls._horizontal else [[g] for g in glyphs]

        params = cls.get_params_cls()(
            rows=rows, spacing=spacing, padding=padding, center=center
        )
        return cls(glyph_id=glyph_id, params=params)


class HArrayGlyph(BaseArrayGlyph):
    _horizontal = True


class VArrayGlyph(BaseArrayGlyph):
    _horizontal = False
