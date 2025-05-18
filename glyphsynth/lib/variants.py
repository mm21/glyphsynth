"""
Functionality to create glyphs with user-defined parameter variations.
For visualization, all variants can be represented as a matrix and a
set of arrays.
"""

from pathlib import Path
from typing import Generator

from ..core import BaseDrawing, BaseParams
from ..core._utils import extract_type_param
from ..core.export import ExportSpec
from .array import HArrayDrawing, VArrayDrawing
from .matrix import MatrixDrawing
from .utils import PaddingDrawing

__all__ = [
    "BaseVariantFactory",
    "BaseVariantExportFactory",
]


class BaseVariantFactory[DrawingT: BaseDrawing]:
    """
    Encapsulates a BaseDrawing subclass and parameter variants.
    """

    _glyph_cls: type[DrawingT]
    """
    BaseDrawing subclass to instantiate.
    """

    def create_matrix_glyph(
        self,
        drawing_id: str | None = None,
        width: int = 1,
        spacing: float = 0.0,
        padding: float = 0.0,
    ) -> MatrixDrawing:
        """
        Creates a matrix drawing of the provided width by iterating over all
        variants.
        """
        rows: list[list[DrawingT]] = []

        # get list of all glyphs
        all_glyphs: list[DrawingT] = list(self.get_variants())

        col_count = width
        row_count = len(all_glyphs) // col_count

        for row_idx in range(row_count):
            rows.append(
                all_glyphs[row_idx * col_count : (row_idx + 1) * col_count]
            )

        # create matrix drawing
        return MatrixDrawing.new(
            rows, drawing_id=drawing_id, spacing=spacing, padding=padding
        )

    def get_variants(self) -> Generator[DrawingT, None, None]:
        """
        Yield all variants.
        """
        for params in self.get_params_variants():
            drawing_id = _derive_glyph_id(params)
            yield self._glyph_cls(drawing_id=drawing_id, params=params)

    def get_params_variants(self) -> Generator[BaseParams, None, None]:
        """
        Override to yield parameter variants to export.
        """
        yield self._glyph_cls.get_params_cls()()

    def __init_subclass__(cls):
        """
        Populate _glyph_cls with the parameterized class.
        """
        glyph_cls = extract_type_param(cls, BaseDrawing)
        assert glyph_cls is not None

        cls._glyph_cls = glyph_cls


class BaseVariantExportFactory[DrawingT: BaseDrawing](
    BaseVariantFactory[DrawingT]
):
    """
    Encapsulates a variant factory which creates and exports arrays of
    glyphs with combinations of drawing parameters and properties.

    Exports a hierarchy of drawing variants:

    - all/[drawing_id].[svg/png]
    - matrix/
        - All glyphs combined in matrix
    - harrays/
        - Horizontal arrays
    - varrays/
        - Vertical arrays
    """

    MATRIX_WIDTH: int = 1
    """
    Width of the resulting matrix drawing. If kept as the default of 1, creates a
    vertical array.

    If set, should equal the number of elements in outermost dimension 
    of the drawing iterable output.

    If a dynamic value is required, override the property `matrix_width`.
    """

    SPACING: int = 0
    """
    Spacing to use between variants.
    """

    def __iter__(self) -> Generator[ExportSpec, None, None]:
        """
        Yield export specs for each variant given by
        concrete VariantFactory.
        """

        def wrap_padding(drawing: BaseDrawing):
            return PaddingDrawing.new(drawing, padding=self.SPACING)

        # lists of arrays
        harray_glyphs: list[HArrayDrawing] = []
        varray_glyphs: list[VArrayDrawing] = []

        # relative paths for exporting
        variants_path = Path("variants")
        all_path = variants_path / "all"
        harrays_path = variants_path / "harrays"
        varrays_path = variants_path / "varrays"
        matrix_path = variants_path / "matrix"

        matrix_glyph = self.create_matrix_glyph(
            drawing_id="matrix",
            width=self.matrix_width,
            spacing=self.SPACING,
            padding=self.SPACING,
        )

        # create array glyphs
        for i, row in enumerate(matrix_glyph.rows):
            harray_glyphs.append(
                HArrayDrawing.new(
                    row,
                    drawing_id=f"row_{i}",
                    spacing=self.SPACING,
                    padding=self.SPACING,
                )
            )

        for i, col in enumerate(matrix_glyph.cols):
            varray_glyphs.append(
                VArrayDrawing.new(
                    col,
                    drawing_id=f"col_{i}",
                    spacing=self.SPACING,
                    padding=self.SPACING,
                )
            )

        # export top-level glyphs
        yield from (
            ExportSpec(wrap_padding(g), all_path, module=type(self).__module__)
            for row in matrix_glyph.rows
            for g in row
        )

        # export horizontal arrays
        for harray_glyph in harray_glyphs:
            yield ExportSpec(
                harray_glyph,
                harrays_path,
                module=type(self).__module__,
            )

        # export vertical arrays
        for varray_glyph in varray_glyphs:
            yield ExportSpec(
                varray_glyph,
                varrays_path,
                module=type(self).__module__,
            )

        # export matrix drawing
        yield ExportSpec(
            matrix_glyph,
            matrix_path,
            module=type(self).__module__,
        )

    @property
    def matrix_width(self) -> int:
        """
        Accessor for the attribute `MATRIX_WIDTH`, but can be overridden if
        a dynamic value is needed.
        """
        return self.MATRIX_WIDTH


def _derive_glyph_id(params: BaseParams) -> str:
    """
    Derive a drawing_id from params.
    """
    return params.desc
