from pathlib import Path

from glyphsynth.lib import HArrayDrawing, VArrayDrawing

from ..conftest import write_drawing
from ..glyphs import UNIT, ParentDrawing

GLYPH_COUNT = 4


def test_basic(output_dir: Path):
    """
    Create horizontal and vertical arrays of basic glyphs.
    """

    h_glyphs: list[ParentDrawing] = []
    v_glyphs: list[ParentDrawing] = []

    for i in range(GLYPH_COUNT):
        h_glyph = ParentDrawing()
        v_glyph = ParentDrawing()

        # rotate every other drawing
        if (i % 2) == 1:
            h_glyph.rotate(180)
            v_glyph.rotate(180)

        h_glyphs.append(h_glyph)
        v_glyphs.append(v_glyph)

    h_array = HArrayDrawing.new(
        glyphs=h_glyphs, spacing=UNIT / 10, padding=UNIT / 10
    )
    v_array = VArrayDrawing.new(
        glyphs=v_glyphs, spacing=UNIT / 10, padding=UNIT / 10
    )

    write_drawing(output_dir, h_array)
    write_drawing(output_dir, v_array)
