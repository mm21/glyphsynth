"""
Functionality to create glyphs with user-defined parameter variations.
For visualization, all variants can be represented as a matrix and a
set of arrays.
"""

from pathlib import Path
from typing import Generator

from ..core import BaseGlyph, BaseParams
from ..core._utils import extract_type_param
from ..core.export import ExportSpec
from .array import HArrayGlyph, VArrayGlyph
from .matrix import MatrixGlyph
from .utils import PaddingGlyph

__all__ = [
    "BaseVariantFactory",
    "BaseVariantExportFactory",
]


class BaseVariantFactory[GlyphT: BaseGlyph]:
    """
    Encapsulates a BaseGlyph subclass and parameter variants.
    """

    _glyph_cls: type[GlyphT]
    """
    BaseGlyph subclass to instantiate.
    """

    def create_matrix_glyph(
        self,
        glyph_id: str | None = None,
        width: int = 1,
        spacing: float = 0.0,
        padding: float = 0.0,
    ) -> MatrixGlyph:
        """
        Creates a matrix glyph of the provided width by iterating over all
        variants.
        """
        rows: list[list[GlyphT]] = []

        # get list of all glyphs
        all_glyphs: list[GlyphT] = list(self.get_variants())

        col_count = width
        row_count = len(all_glyphs) // col_count

        for row_idx in range(row_count):
            rows.append(
                all_glyphs[row_idx * col_count : (row_idx + 1) * col_count]
            )

        # create matrix glyph
        return MatrixGlyph.new(
            rows, glyph_id=glyph_id, spacing=spacing, padding=padding
        )

    def get_variants(self) -> Generator[GlyphT, None, None]:
        """
        Yield all variants.
        """
        for params in self.get_params_variants():
            glyph_id = _derive_glyph_id(params)
            yield self._glyph_cls(glyph_id=glyph_id, params=params)

    def get_params_variants(self) -> Generator[BaseParams, None, None]:
        """
        Override to yield parameter variants to export.
        """
        yield self._glyph_cls.get_params_cls()()

    def __init_subclass__(cls):
        """
        Populate _glyph_cls with the parameterized class.
        """
        glyph_cls = extract_type_param(cls, BaseGlyph)
        assert glyph_cls is not None

        cls._glyph_cls = glyph_cls


class BaseVariantExportFactory[GlyphT: BaseGlyph](BaseVariantFactory[GlyphT]):
    """
    Encapsulates a variant factory which creates and exports arrays of
    glyphs with combinations of glyph parameters and properties.

    Exports a hierarchy of glyph variants:

    - all/[glyph_id].[svg/png]
    - matrix/
        - All glyphs combined in matrix
    - harrays/
        - Horizontal arrays
    - varrays/
        - Vertical arrays
    """

    MATRIX_WIDTH: int = 1
    """
    Width of the resulting matrix glyph. If kept as the default of 1, creates a
    vertical array.

    If set, should equal the number of elements in outermost dimension 
    of the glyph iterable output.

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

        def wrap_padding(glyph: BaseGlyph):
            return PaddingGlyph.new(glyph, padding=self.SPACING)

        # lists of arrays
        harray_glyphs: list[HArrayGlyph] = []
        varray_glyphs: list[VArrayGlyph] = []

        # relative paths for exporting
        variants_path = Path("variants")
        all_path = variants_path / "all"
        harrays_path = variants_path / "harrays"
        varrays_path = variants_path / "varrays"
        matrix_path = variants_path / "matrix"

        matrix_glyph = self.create_matrix_glyph(
            glyph_id="matrix",
            width=self.matrix_width,
            spacing=self.SPACING,
            padding=self.SPACING,
        )

        # create array glyphs
        for i, row in enumerate(matrix_glyph.rows):
            harray_glyphs.append(
                HArrayGlyph.new(
                    row,
                    glyph_id=f"row_{i}",
                    spacing=self.SPACING,
                    padding=self.SPACING,
                )
            )

        for i, col in enumerate(matrix_glyph.cols):
            varray_glyphs.append(
                VArrayGlyph.new(
                    col,
                    glyph_id=f"col_{i}",
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

        # export matrix glyph
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
    Derive a glyph_id from params.
    """
    return params.desc
