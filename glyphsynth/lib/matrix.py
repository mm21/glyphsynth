from ..core import BaseGlyph, BaseParams

__all__ = [
    "MatrixParams",
    "MatrixGlyph",
]


class MatrixParams(BaseParams):
    rows: list[list[BaseGlyph]]
    spacing: float = 0.0
    padding: float = 0.0
    center: bool = True


class BaseMatrixGlyph(BaseGlyph[MatrixParams]):
    """
    Base matrix class, used for matrix glyph and array glyphs.
    """

    _rows: list[list[BaseGlyph]]
    _cols: list[list[BaseGlyph]]

    _max_width: float
    _max_height: float

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

        for row_idx, row in enumerate(self._rows):
            for col_idx, glyph in enumerate(row):
                insert_x: float
                insert_y: float

                # set insert point
                insert_x = col_idx * (self._max_width + self.params.spacing)
                insert_y = row_idx * (self._max_height + self.params.spacing)

                # adjust insert point if centered
                if self.params.center:
                    insert_x += (self._max_width - glyph.size[0]) / 2
                    insert_y += (self._max_height - glyph.size[1]) / 2

                # add padding
                insert_x += self.params.padding
                insert_y += self.params.padding

                # insert glyph
                self.insert_glyph(glyph, (insert_x, insert_y))

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

        # add padding
        width += self.params.padding * 2
        height += self.params.padding * 2

        return (width, height)


class MatrixGlyph(BaseMatrixGlyph):
    """
    Glyph encapsulating a matrix of glyphs with constant spacing between them
    and padding around the edges.

    If `center` is `True`, glyphs are center aligned.
    """

    @classmethod
    def new(
        cls,
        rows: list[list[BaseGlyph]],
        glyph_id: str | None = None,
        spacing: float = 0.0,
        padding: float = 0.0,
        center: bool = True,
    ):
        params = cls.get_params_cls()(
            rows=rows, spacing=spacing, padding=padding, center=center
        )
        return cls(glyph_id=glyph_id, params=params)

    @property
    def rows(self) -> list[list[BaseGlyph]]:
        return self._rows

    @property
    def cols(self) -> list[list[BaseGlyph]]:
        return self._cols
