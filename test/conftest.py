import logging
import os
from pathlib import Path

from pytest import fixture, FixtureRequest

from glyphsynth import (
    BaseGlyph,
    RASTER_SUPPORT,
)
from glyphsynth.lib.arrays import HArrayGlyph, VArrayGlyph
from glyphsynth.lib.alphabet.minimal import UNIT

logging.basicConfig(level=logging.DEBUG)

OUTPUT_PATH = Path(os.getcwd()) / "test" / "__build__"
SPACING: float = UNIT / 10


def write_glyph(output_dir: Path, glyph: BaseGlyph):
    glyph.export_svg(output_dir)
    glyph.export_png(output_dir)


def write_glyphs(output_dir: Path, glyphs: list[BaseGlyph]):
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


@fixture
def output_dir(request: FixtureRequest) -> Path:
    # get path to test folder
    test_path = Path(os.getcwd()) / "test"

    # get path to this test
    fspath = Path(request.node.fspath)

    testcase_path = fspath.parent / fspath.stem / request.node.name

    # get containing path relative to test folder
    # rel_path =

    # get output path and ensure it exists
    output_path = OUTPUT_PATH / testcase_path.relative_to(test_path)
    output_path.mkdir(parents=True, exist_ok=True)

    return output_path
