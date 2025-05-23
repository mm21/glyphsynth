from pathlib import Path

from pytest import mark, raises

from glyphsynth import RASTER_SUPPORT, Drawing, Properties
from glyphsynth.drawing.export import export_drawings

from .conftest import write_drawing
from .glyphs import (
    UNIT,
    BasicDrawing,
    BasicParams,
    GradientDrawing,
    ParentDrawing,
    ParentDrawing2,
)


def test_basic(output_dir: Path):
    """
    Create basic drawing.
    """

    drawing = BasicDrawing()
    write_drawing(output_dir, drawing)


def test_basic_rescaled(output_dir: Path):
    """
    Create basic drawing and rescale in a parent drawing.
    """

    drawing = BasicDrawing(size=(UNIT * 10, UNIT * 10))
    write_drawing(output_dir, drawing)


def test_params():
    """
    Create glyphs with parameters.
    """

    glyph1: BasicDrawing = BasicDrawing()

    params2: BasicParams = BasicParams()
    glyph2: BasicDrawing = BasicDrawing(params=params2)

    params3: BasicParams = BasicParams(color1="red")
    glyph3: BasicDrawing = BasicDrawing(params=params3)

    assert glyph1.params.color1 == "black"
    assert glyph1.properties.stroke == "black"

    assert glyph2.params.color1 == "black"
    assert glyph2.properties.stroke == "black"

    assert glyph3.params.color1 == "red"
    assert glyph3.properties.stroke == "red"


def test_params_default():
    """
    Create a drawing with default parameters.
    """

    class BasicDrawingTest(BasicDrawing):
        default_params = BasicParams(
            color1="red",
        )

    drawing = BasicDrawingTest()
    assert drawing.params.color1 == "red"


def test_props():
    """
    Create drawing with properties.
    """

    properties1: Properties = Properties(fill="red")
    glyph1: BasicDrawing = BasicDrawing(properties=properties1)

    assert glyph1.properties.fill == "red"


def test_composition(output_dir: Path):
    """
    Create drawing with sub-glyphs.
    """

    parent = ParentDrawing()

    assert parent._nested_glyphs[0] is parent.child1
    assert parent._nested_glyphs[1] is parent.child2

    assert parent.child1.params.color1 == "black"
    assert parent.child2.params.color1 == "red"

    write_drawing(output_dir, parent)


def test_composition_rescaled(output_dir: Path):
    """
    Create drawing with rescaled sub-glyphs.
    """

    parent = ParentDrawing2()
    write_drawing(output_dir, parent)


@mark.skipif(
    RASTER_SUPPORT is False, reason="Rasterizing only supported on linux"
)
def test_raster(output_dir):
    """
    Create drawing and save to png.
    """

    parent: ParentDrawing = ParentDrawing()

    parent.export_png(output_dir)


def test_empty(output_dir: Path):
    """
    Verify Drawing, with and without explicit size.
    """

    glyph1 = Drawing(drawing_id="glyph1")
    glyph2 = Drawing(drawing_id="glyph2", size=(UNIT * 2, UNIT * 2))

    for drawing in [glyph1, glyph2]:
        drawing.insert_drawing(ParentDrawing())
        drawing.insert_drawing(ParentDrawing(), (UNIT, UNIT))

        write_drawing(output_dir, drawing)


def test_export(output_dir: Path):
    drawing = BasicDrawing()

    drawing.export(output_dir / "basic-auto")
    drawing.export(output_dir / "basic.svg")
    drawing.export(output_dir / "basic.png")

    with raises(ValueError):
        drawing.export(output_dir / "fractal-test.invalid")

    export_drawings(
        "test.glyphs.BasicDrawing",
        output_dir / "basic",
        output_modpath=True,
        svg=True,
        png=True,
    )

    export_drawings(
        "test.glyphs",
        output_dir / "glyphs",
        output_modpath=True,
        svg=True,
        png=True,
    )


def test_gradient(output_dir: Path):
    drawing = GradientDrawing()
    write_drawing(output_dir, drawing)
