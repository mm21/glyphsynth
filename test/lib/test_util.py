from pathlib import Path

from glyphsynth.lib import PaddingDrawing

from ..conftest import write_drawing
from ..glyphs import ParentDrawing


def test_padding(output_dir: Path):
    glyph_inner = ParentDrawing()
    drawing = PaddingDrawing.new(glyph_inner)

    write_drawing(output_dir, drawing)
