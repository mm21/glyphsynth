from ..drawing import BaseDrawing, BaseParams

__all__ = [
    "MatrixParams",
    "MatrixDrawing",
]


class MatrixParams(BaseParams):
    rows: list[list[BaseDrawing]]
    spacing: float = 0.0
    padding: float = 0.0
    center: bool = True


class BaseMatrixDrawing(BaseDrawing[MatrixParams]):
    """
    Base matrix class, used for matrix drawing and array glyphs.
    """

    _rows: list[list[BaseDrawing]]
    _cols: list[list[BaseDrawing]]

    _max_width: float
    _max_height: float

    def init(self):
        # validate rows
        for i, row in enumerate(self.params.rows):
            assert len(row) == len(
                self.params.rows[i - 1]
            ), f"Row lengths inconsistent: {self.params.rows}"

        self.canonical_size = self._get_size()

    def draw(self):
        if len(self.params.rows) == 0:
            return

        for row_idx, row in enumerate(self._rows):
            for col_idx, drawing in enumerate(row):
                insert_x: float
                insert_y: float

                # set insert point
                insert_x = col_idx * (self._max_width + self.params.spacing)
                insert_y = row_idx * (self._max_height + self.params.spacing)

                # adjust insert point if centered
                if self.params.center:
                    insert_x += (self._max_width - drawing.size[0]) / 2
                    insert_y += (self._max_height - drawing.size[1]) / 2

                # add padding
                insert_x += self.params.padding
                insert_y += self.params.padding

                # insert drawing
                self.insert_drawing(drawing, (insert_x, insert_y))

    def _get_size(self) -> tuple[float, float]:
        """
        Get the size of this matrix based on the sizes of the glyphs.
        """

        width: float
        height: float

        if len(self.params.rows) == 0:
            return (0.0, 0.0)

        rows: list[list[BaseDrawing]] = list(
            [list(row) for row in self.params.rows]
        )
        cols: list[list[BaseDrawing]] = list(map(list, zip(*rows)))

        # get column widths
        col_widths = [max([d.size[0] for d in col]) for col in cols]

        # get row heights
        row_heights = [max([d.size[1] for d in row]) for row in rows]

        # set rows/cols
        self._rows = rows
        self._cols = cols

        # get max width/height
        self._max_width = max(col_widths)
        self._max_height = max(row_heights)

        # get total width
        width = self._max_width * len(cols) + self.params.spacing * (
            len(cols) - 1
        )

        # get total height
        height = self._max_height * len(rows) + self.params.spacing * (
            len(rows) - 1
        )

        # add padding
        width += self.params.padding * 2
        height += self.params.padding * 2

        return (width, height)


class MatrixDrawing(BaseMatrixDrawing):
    """
    Drawing encapsulating a matrix of glyphs with constant spacing between them
    and padding around the edges.

    If `center` is `True`, glyphs are center aligned.
    """

    @classmethod
    def new(
        cls,
        rows: list[list[BaseDrawing]],
        drawing_id: str | None = None,
        spacing: float = 0.0,
        padding: float = 0.0,
        center: bool = True,
    ):
        params = cls.get_params_cls()(
            rows=rows, spacing=spacing, padding=padding, center=center
        )
        return cls(drawing_id=drawing_id, params=params)

    @property
    def rows(self) -> list[list[BaseDrawing]]:
        return self._rows

    @property
    def cols(self) -> list[list[BaseDrawing]]:
        return self._cols
