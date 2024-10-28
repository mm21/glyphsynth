from abc import ABC
from typing import Iterable

from ..core import BaseGlyph, BaseParams
from .arrays import HArrayGlyph, VArrayGlyph

__all__ = [
    "MatrixParams",
    "MatrixGlyph",
]


class MatrixParams(BaseParams):
    rows: list[list[BaseGlyph]]
    spacing: float = 0.0
    center: bool = True


class MatrixGlyph(BaseGlyph[MatrixParams]):
    """
    Glyph encapsulating a matrix of glyphs with constant spacing between them.

    If `center` is `True`, glyphs are center aligned.
    """

    _rows: list[list[BaseGlyph]]
    _cols: list[list[BaseGlyph]]

    _max_width: float
    _max_height: float

    @classmethod
    def new(
        cls,
        rows: Iterable[Iterable[BaseGlyph]],
        glyph_id: str | None = None,
        spacing: float = 0.0,
        center: bool = True,
    ):
        params = cls.get_params_cls()(rows=rows, spacing=spacing, center=center)
        return cls(params=params, glyph_id=glyph_id)

    def init(self):
        # validate rows
        for i, row in enumerate(self.params.rows):
            assert len(row) == len(
                self.params.rows[i - 1]
            ), f"Row lengths inconsistent: {self.params.rows}"

        self.size_canon = self._get_size()

    def draw(self):
        if len(self.params.rows) == 0:
            return

        insert: tuple[float, float]

        for row_idx, row in enumerate(self._rows):
            for col_idx, glyph in enumerate(row):
                # set insert point
                insert = (
                    col_idx * (self._max_width + self.params.spacing),
                    row_idx * (self._max_height + self.params.spacing),
                )

                # adjust insert point if centered
                if self.params.center:
                    insert = (
                        insert[0] + (self._max_width - glyph.size[0]) / 2,
                        insert[1] + (self._max_height - glyph.size[1]) / 2,
                    )

                # insert glyph
                self.insert_glyph(glyph, insert)

    def _get_size(self) -> tuple[float, float]:
        """
        Get the size of this matrix based on the sizes of the glyphs.
        """

        width: float
        height: float

        if len(self.params.rows) == 0:
            return (0.0, 0.0)

        rows: list[list[BaseGlyph]] = list(
            [list(row) for row in self.params.rows]
        )
        cols: list[list[BaseGlyph]] = list(map(list, zip(*rows)))

        # get column widths
        col_widths = [max([g.size[0] for g in col]) for col in cols]

        # get row heights
        row_heights = [max([g.size[1] for g in row]) for row in rows]

        # set rows/cols
        self._rows = rows
        self._cols = cols

        # get max width/height
        self._max_width = max(col_widths)
        self._max_height = max(row_heights)

        # get total width
        width = sum(col_widths) + self.params.spacing * (len(cols) - 1)

        # get total height
        height = sum(row_heights) + self.params.spacing * (len(rows) - 1)

        return (width, height)

    def _align_insert(
        self, insert: tuple[float, float], glyph: BaseGlyph
    ) -> tuple[float, float]:
        """
        Center this glyph as needed.
        """

        x: float
        y: float

        x, y = insert

        if self.params.center:
            x += (self._max_width - glyph.size[0]) / 2
            y += (self._max_height - glyph.size[1]) / 2

        return (x, y)

    def _advance_insert(
        self, insert: tuple[float, float], glyph: BaseGlyph
    ) -> tuple[float, float]:
        """
        Advance insert point to the point for the next glyph, not considering
        any alignment.
        """

        # TODO