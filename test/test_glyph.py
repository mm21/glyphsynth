from pathlib import Path

from pytest import mark

from glyphsynth import RASTER_SUPPORT, EmptyGlyph, Properties
from glyphsynth.core.export import export_glyphs

from .conftest import write_glyph
from .glyphs import UNIT, BasicGlyph, BasicParams, ParentGlyph, ParentGlyph2


def test_basic(output_dir: Path):
    """
    Create basic glyph.
    """

    glyph = BasicGlyph()
    write_glyph(output_dir, glyph)


def test_basic_rescaled(output_dir: Path):
    """
    Create basic glyph and rescale in a parent glyph.
    """

    glyph = BasicGlyph(size=(UNIT * 10, UNIT * 10))
    write_glyph(output_dir, glyph)


def test_params():
    """
    Create glyphs with parameters.
    """

    glyph1: BasicGlyph = BasicGlyph()

    params2: BasicParams = BasicParams()
    glyph2: BasicGlyph = BasicGlyph(params=params2)

    params3: BasicParams = BasicParams(color1="red")
    glyph3: BasicGlyph = BasicGlyph(params=params3)

    assert glyph1.params.color1 == "black"
    assert glyph1.properties.color == "black"

    assert glyph2.params.color1 == "black"
    assert glyph2.properties.color == "black"

    assert glyph3.params.color1 == "red"
    assert glyph3.properties.color == "red"


def test_params_default():
    """
    Create a glyph with default parameters.
    """

    class BasicGlyphTest(BasicGlyph):
        class DefaultParams(BasicParams):
            color1: str = "red"

    glyph = BasicGlyphTest()
    assert glyph.params.color1 == "red"


def test_props():
    """
    Create glyph with properties.
    """

    properties1: Properties = Properties(fill="red")
    glyph1: BasicGlyph = BasicGlyph(properties=properties1)

    assert glyph1.properties.fill == "red"


def test_composition(output_dir: Path):
    """
    Create glyph with sub-glyphs.
    """

    parent = ParentGlyph()

    assert parent._nested_glyphs[0] is parent.child1
    assert parent._nested_glyphs[1] is parent.child2

    assert parent.child1.params.color1 == "black"
    assert parent.child2.params.color1 == "red"

    write_glyph(output_dir, parent)


def test_composition_rescaled(output_dir: Path):
    """
    Create glyph with rescaled sub-glyphs.
    """

    parent = ParentGlyph2()
    write_glyph(output_dir, parent)


@mark.skipif(
    RASTER_SUPPORT is False, reason="Rasterizing only supported on linux"
)
def test_raster(output_dir):
    """
    Create glyph and save to png.
    """

    parent: ParentGlyph = ParentGlyph()

    parent.export_png(output_dir)


def test_empty(output_dir: Path):
    """
    Verify EmptyGlyph, with and without explicit size.
    """

    glyph1 = EmptyGlyph(glyph_id="glyph1")
    glyph2 = EmptyGlyph(glyph_id="glyph2", size=(UNIT * 2, UNIT * 2))

    for glyph in [glyph1, glyph2]:
        glyph.insert_glyph(ParentGlyph())
        glyph.insert_glyph(ParentGlyph(), (UNIT, UNIT))

        glyph.export_svg(output_dir)
        glyph.export_png(output_dir)


def test_export(output_dir: Path):
    export_glyphs(
        "test.glyphs.BasicGlyph",
        output_dir,
        output_modpath=True,
        svg=True,
        png=True,
    )

    export_glyphs(
        "test.glyphs",
        output_dir,
        output_modpath=True,
        svg=True,
        png=True,
    )
