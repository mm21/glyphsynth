from pathlib import Path

from glyphsynth import ShapeProperties

from .conftest import write_glyph
from .glyphs import HALF, UNIT, BasicGlyph


def test_group(output_dir: Path):
    glyph = BasicGlyph()

    g1 = glyph.create_group()
    g2 = glyph.create_group()

    g1.draw_circle(
        (HALF, HALF), UNIT / 3, properties=ShapeProperties(fill="green")
    )
    g2.draw_circle(
        (HALF, HALF), UNIT / 4, properties=ShapeProperties(fill="blue")
    )

    write_glyph(output_dir, glyph)
