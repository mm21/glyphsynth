import logging
import os
from pathlib import Path

from pytest import FixtureRequest, fixture

from glyphsynth import RASTER_SUPPORT, BaseGlyph
from glyphsynth.lib.alphabet.minimal import UNIT
from glyphsynth.lib.arrays import HArrayGlyph, VArrayGlyph

logging.basicConfig(level=logging.DEBUG)

OUTPUT_PATH = Path(os.getcwd()) / "test" / "__out__"
SPACING: float = UNIT / 10


# TODO: after writing, verify svg with golden svg
# - doit task to update golden svg w/testcase output
def write_glyph(
    output_dir: Path, glyph: BaseGlyph, stem: str | None = None, scale: int = 1
):
    svg_path = output_dir / f"{stem}.svg" if stem else output_dir
    png_path = output_dir / f"{stem}.png" if stem else output_dir

    glyph.export_svg(svg_path)

    if RASTER_SUPPORT:
        glyph.export_png(png_path, scale=scale)


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
