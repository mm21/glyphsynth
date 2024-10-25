import logging
import os
from pathlib import Path

from pytest import fixture, FixtureRequest

from glyphsynth import (
    BaseParams,
    BaseGlyph,
    Properties,
    PropertyValue,
    RASTER_SUPPORT,
)
from glyphsynth.lib.arrays import HArrayGlyph, VArrayGlyph
from glyphsynth.lib.alphabet.minimal import (
    UNIT,
    ZERO,
)


from glyphsynth.core.glyph import id_factory

logging.basicConfig(level=logging.DEBUG)

OUTPUT_PATH = Path(os.getcwd()) / "test" / "__build__"
SPACING: float = UNIT / 10


def write_glyphs(output_dir: str, glyphs: list[BaseGlyph]):
    """
    Create horizontal and vertical arrays and save them to the provided path,
    in addition to an svg per individual glyph.
    """

    # write arrays
    array_h = HArrayGlyph.new(glyphs, spacing=SPACING)
    array_v = VArrayGlyph.new(glyphs, spacing=SPACING)

    array_h.export_svg(output_dir / "_array-h.svg")
    array_v.export_svg(output_dir / "_array-v.svg")

    if RASTER_SUPPORT:
        array_h.export_png(output_dir / "_array-h.png")
        array_v.export_png(output_dir / "_array-v.png")
    else:
        logging.warning("Skipping rasterizing")

    # write individual glyphs
    for glyph in glyphs:
        glyph.export_svg(output_dir)


BASIC_STROKE_PCT: float = 5.0
BASIC_STROKE_WIDTH: float = BASIC_STROKE_PCT * UNIT
BASIC_STROKE_HALF: float = BASIC_STROKE_WIDTH / 2


class BasicParams(BaseParams):
    color1: str = "black"


class BasicGlyph(BaseGlyph[BasicParams]):
    class DefaultProperties(Properties):
        stroke: PropertyValue = "black"
        stroke_width: PropertyValue = str(BASIC_STROKE_WIDTH)

    size_canon = (UNIT, UNIT)

    def init(self):
        self.properties.color = self.params.color1
        self.properties.stroke = self.params.color1

    def draw(self):
        self.draw_polyline(
            [(ZERO, BASIC_STROKE_HALF), (UNIT, BASIC_STROKE_HALF)]
        )


class ParentGlyph(BaseGlyph):
    child1: BasicGlyph
    child2: BasicGlyph

    size_canon = BasicGlyph.size_canon

    def draw(self):
        params2: BasicParams = BasicParams(color1="red")

        self.child1 = BasicGlyph(size=self.size_canon, parent=self)
        self.child2 = BasicGlyph(
            size=self.size_canon, params=params2, parent=self
        )

        # rotate child2
        self.child2.rotate(180.0)


class ParentGlyph2(ParentGlyph):
    def init(self):
        assert BasicGlyph.size_canon is not None
        self.size_canon = (
            BasicGlyph.size_canon[0] * 10,
            BasicGlyph.size_canon[1] * 10,
        )


@fixture(autouse=True)
def id_reset():
    """
    Reset id_factory after each test is completed.
    """
    yield
    id_factory.reset()


@fixture
def output_dir(request: FixtureRequest) -> Path:
    # get path to test folder
    test_path = Path(os.getcwd()) / "test"

    # get path to this test
    fspath = Path(request.node.fspath)

    # get containing path relative to test folder
    rel_path = fspath.parent.relative_to(test_path)

    # get output path and ensure it exists
    output_path = OUTPUT_PATH / rel_path / request.node.name
    output_path.mkdir(parents=True, exist_ok=True)

    return output_path
