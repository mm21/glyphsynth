import os

from pytest import mark

from glyphsynth import EmptyGlyph, Properties, RASTER_SUPPORT

from .conftest import BasicParams, BasicGlyph, ParentGlyph, ParentGlyph2, UNIT


def test_basic(output_dir: str):
    """
    Create basic glyph.
    """

    glyph = BasicGlyph()
    glyph.export_svg(output_dir)


def test_basic_rescaled(output_dir: str):
    """
    Create basic glyph and rescale in a parent glyph.
    """

    glyph = BasicGlyph(size=(UNIT * 10, UNIT * 10))
    glyph.export_svg(output_dir)


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


def test_composition(output_dir: str):
    """
    Create glyph with sub-glyphs.
    """

    parent: ParentGlyph = ParentGlyph()

    assert parent.child1._parent is parent
    assert parent.child2._parent is parent

    assert parent.child1.params.color1 == "black"
    assert parent.child2.params.color1 == "red"

    parent.export_svg(output_dir)


def test_composition_rescaled(output_dir: str):
    """
    Create glyph with rescaled sub-glyphs.
    """

    parent: ParentGlyph2 = ParentGlyph2()
    parent.export_svg(output_dir)


@mark.skipif(
    RASTER_SUPPORT is False, reason="Rasterizing only supported on linux"
)
def test_raster(output_dir):
    """
    Create glyph and save to png.
    """

    parent: ParentGlyph = ParentGlyph()

    parent.export_png(output_dir)


def test_empty(output_dir: str):
    """
    Verify EmptyGlyph.
    """

    glyph = EmptyGlyph()

    glyph.insert_glyph(ParentGlyph())
    glyph.insert_glyph(ParentGlyph(), (UNIT, UNIT))

    glyph.export_svg(output_dir)


"""
def test_draw():

    glyph = EmptyGlyph()
    params: BasicParams = BasicParams()
    params2: EmptyParams = EmptyParams()
    parent: ParentGlyph = glyph.draw_glyph(ParentGlyph, params2)

    print(f'--- parent: {parent}')
"""
