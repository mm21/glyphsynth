from pathlib import Path

from glyphsynth import EmptyGlyph, ShapeProperties

from .conftest import write_glyph
from .glyphs import HALF, ORIGIN, UNIT, BasicGlyph


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


def test_fill(output_dir: Path):
    glyph = EmptyGlyph(size=(UNIT, UNIT))

    gradient1 = glyph.create_linear_gradient(
        start=ORIGIN, end=(UNIT, UNIT), colors=["red", "purple"]
    )
    gradient2 = glyph.create_radial_gradient(
        center=(HALF, HALF),
        radius=HALF,
        focal=(HALF / 2, HALF / 2),
        colors=["blue", "yellow"],
    )

    rect = glyph.draw_rect(ORIGIN, (UNIT, UNIT))
    rect.fill(gradient=gradient1)

    circle = glyph.draw_circle(
        (HALF, HALF), HALF, properties=ShapeProperties(opacity="0.8")
    )
    circle.fill(gradient=gradient2)

    write_glyph(output_dir, glyph)
