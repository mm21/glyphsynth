from pytest import mark

from glyphsynth import BaseGlyph, BaseParams, Properties, PropertyValue
from glyphsynth.lib import ArrayParams, HArrayGlyph, VArrayGlyph

from ..conftest import ParentGlyph, UNIT

GLYPH_COUNT = 4


def test_basic(output_dir: str):
    """
    Create horizontal and vertical arrays of basic glyphs.
    """

    h_glyphs: list[ParentGlyph] = []
    v_glyphs: list[ParentGlyph] = []

    for i in range(GLYPH_COUNT):
        h_glyph = ParentGlyph()
        v_glyph = ParentGlyph()

        # rotate every other glyph
        if (i % 2) == 1:
            h_glyph.rotate(180)
            v_glyph.rotate(180)

        h_glyphs.append(h_glyph)
        v_glyphs.append(v_glyph)

    h_array_params: ArrayParams = ArrayParams(
        glyphs=h_glyphs, spacing=UNIT / 10
    )

    v_array_params: ArrayParams = ArrayParams(
        glyphs=v_glyphs, spacing=UNIT / 10
    )

    h_array: HArrayGlyph = HArrayGlyph(params=h_array_params)
    v_array: VArrayGlyph = VArrayGlyph(params=v_array_params)

    h_array.export_svg(output_dir)
    v_array.export_svg(output_dir)


def test_scale(output_dir: str):
    # TODO
    # - create glyphs of different scales
    # - create h+v arrays with center=False and center=True (4 total)

    pass
