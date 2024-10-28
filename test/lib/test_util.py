from pathlib import Path

from glyphsynth.lib import PaddingGlyph

from ..conftest import write_glyph
from ..glyphs import ParentGlyph


def test_padding(output_dir: Path):
    glyph_inner = ParentGlyph()
    glyph = PaddingGlyph.new(glyph_inner)

    write_glyph(output_dir, glyph)
