from pathlib import Path

from glyphsynth import Drawing, ShapeProperties

from .conftest import write_drawing
from .glyphs import HALF, ORIGIN, UNIT, BasicDrawing, BasicParams


def test_group(output_dir: Path):
    drawing = BasicDrawing()

    g1 = drawing.create_group()
    g2 = drawing.create_group()

    g1.draw_circle(
        (HALF, HALF), UNIT / 3, properties=ShapeProperties(fill="green")
    )
    g2.draw_circle(
        (HALF, HALF), UNIT / 4, properties=ShapeProperties(fill="blue")
    )

    g1.insert_drawing(
        BasicDrawing(
            params=BasicParams(color1="orange", color2="yellow")
        ).rotate(90)
    )

    write_drawing(output_dir, drawing)


def test_fill(output_dir: Path):
    drawing = Drawing(size=(UNIT, UNIT))

    gradient1 = drawing.create_linear_gradient(
        start=ORIGIN, end=(UNIT, UNIT), colors=["red", "purple"]
    )
    gradient2 = drawing.create_radial_gradient(
        center=(HALF, HALF),
        radius=HALF,
        focal=(HALF / 2, HALF / 2),
        colors=["blue", "yellow"],
    )

    rect = drawing.draw_rect(ORIGIN, (UNIT, UNIT))
    rect.fill(gradient=gradient1)

    circle = drawing.draw_circle(
        (HALF, HALF), HALF, properties=ShapeProperties(opacity=0.8)
    )
    circle.fill(gradient=gradient2)

    write_drawing(output_dir, drawing)
