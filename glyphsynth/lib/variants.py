"""
Functionality to create glyphs with user-defined parameter variations.
For visualization, all variants can be represented as a matrix and a
set of arrays.
"""

import itertools
from pathlib import Path
from typing import Generator

from ..core.export import ExportSpec

from glyphsynth import (
    BaseGlyph,
    BaseParams,
    Properties,
    HArrayGlyph,
    VArrayGlyph,
    PaddingGlyph,
)


class BaseVariantFactory[GlyphT: BaseGlyph]:
    """
    Encapsulates a BaseGlyph subclass and variants for parameters and
    properties.
    """

    glyph_cls: type[GlyphT]
    """
    BaseGlyph subclass to instantiate.
    """

    def get_variants(self) -> Generator[GlyphT, None, None]:
        """
        Yields all variants.
        """
        for params, properties in itertools.product(
            self.get_params_variants(), self.get_properties_variants()
        ):
            glyph_id = _derive_glyph_id(params, properties)

            yield self.glyph_cls(
                glyph_id=glyph_id, params=params, properties=properties
            )

    def get_params_variants(self) -> Generator[BaseParams, None, None]:
        """
        Override to yield parameter variants to export.
        """
        yield self.glyph_cls.get_params_cls()()

    def get_properties_variants(self) -> Generator[Properties, None, None]:
        """
        Override to yield property variants to export.
        """
        yield self.glyph_cls.DefaultProperties()


class BaseVariantExportFactory[GlyphT: BaseGlyph](BaseVariantFactory[GlyphT]):
    """
    Encapsulates a variant factory which creates and exports arrays of
    glyphs with combinations of glyph parameters and properties.

    Exports a hierarchy of glyph variants:

    - all/[glyph_id].[svg/png]
    - arrays/
        - params/
            - [property_variant.desc]_*.[svg/png]
                - Param variants for each property variant
        - properties/
            - [param_variant.desc]_*.[svg/png]
                - Property variants for each param variant
    - matrix.[svg/png]
        - Combined param + property variants
            - Properties varying horizontally
            - Params varying vertically
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

        # get list of all glyphs
        all_glyphs: list[GlyphT] = list(self.get_variants())

        # length of slices to create as vertical arrays
        v_len = len(all_glyphs) // self.matrix_width

        # length of slices to create as horizontal arrays
        h_len = self.matrix_width

        # list of horizontal arrays
        harrays: list[list[GlyphT]] = [[] for _ in range(h_len)]
        harray_glyphs: list[HArrayGlyph] = []

        # list of vertical arrays
        varrays: list[list[GlyphT]] = [[] for _ in range(v_len)]
        varray_glyphs: list[VArrayGlyph] = []

        # relative paths for exporting
        variants_path = Path("variants")
        all_path = variants_path / "all"
        harrays_path = variants_path / "harrays"
        varrays_path = variants_path / "varrays"
        matrix_path = variants_path / "matrix"

        # create horizontal/vertical arrays
        for i in range(h_len):
            harrays[i] = [all_glyphs[j * v_len + i] for j in range(h_len)]

        for i in range(v_len):
            varrays[i] = all_glyphs[i * v_len : (i + 1) * v_len]

        # create array glyphs from raw arrays
        for i, harray in enumerate(harrays):
            harray_glyphs.append(
                HArrayGlyph.new(
                    harray, glyph_id=f"row_{i}", spacing=self.SPACING
                )
            )

        for i, varray in enumerate(varrays):
            varray_glyphs.append(
                VArrayGlyph.new(
                    varray, glyph_id=f"column_{i}", spacing=self.SPACING
                )
            )

        # export top-level glyphs
        for glyph in all_glyphs:
            yield ExportSpec(
                wrap_padding(glyph), all_path, module=type(self).__module__
            )

        # export horizontal arrays
        for i, harray_glyph in enumerate(harray_glyphs):
            yield ExportSpec(
                wrap_padding(harray_glyph),
                harrays_path,
                module=type(self).__module__,
            )

        # export vertical arrays
        for i, varray_glyph in enumerate(varray_glyphs):
            yield ExportSpec(
                wrap_padding(varray_glyph),
                varrays_path,
                module=type(self).__module__,
            )

        # export matrix glyph as vertical array of horizontal arrays
        yield ExportSpec(
            wrap_padding(
                VArrayGlyph.new(
                    harray_glyphs, glyph_id="matrix", spacing=self.SPACING
                )
            ),
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


def _derive_glyph_id(params: BaseParams, properties: Properties) -> str:
    """
    Derive a glyph_id from params and properties.
    """
    descs: list[str] = [params.desc, properties.desc]

    # filter out empty values
    descs = [d for d in descs if len(d)]

    return "___".join(descs)