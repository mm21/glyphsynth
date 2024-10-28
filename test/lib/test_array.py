from pathlib import Path

from glyphsynth.lib import HArrayGlyph, VArrayGlyph

from ..glyphs import ParentGlyph, UNIT
from ..conftest import write_glyph


GLYPH_COUNT = 4


def test_basic(output_dir: Path):
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

    h_array = HArrayGlyph.new(
        glyphs=h_glyphs, spacing=UNIT / 10, padding=UNIT / 10
    )
    v_array = VArrayGlyph.new(
        glyphs=v_glyphs, spacing=UNIT / 10, padding=UNIT / 10
    )

    write_glyph(output_dir, h_array)
    write_glyph(output_dir, v_array)
