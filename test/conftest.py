import logging
import os
from pathlib import Path

from pytest import FixtureRequest, fixture

from glyphsynth import RASTER_SUPPORT, BaseDrawing
from glyphsynth.glyph.glyph import UNIT
from glyphsynth.lib.array import HArrayDrawing, VArrayDrawing
from glyphsynth.lib.utils import PaddingDrawing

logging.basicConfig(level=logging.INFO)

OUTPUT_PATH = Path(os.getcwd()) / "test" / "__out__"
SPACING: float = UNIT / 10


# TODO: after writing, verify svg with golden svg
# - doit task to update golden svg w/testcase output
def write_drawing(
    output_dir: Path,
    drawing: BaseDrawing,
    stem: str | None = None,
    scale: int = 1,
):
    svg_path = output_dir / f"{stem}.svg" if stem else output_dir
    png_path = output_dir / f"{stem}.png" if stem else output_dir

    drawing.export_svg(svg_path)

    if RASTER_SUPPORT:
        drawing.export_png(png_path, scale=scale)


def write_glyphs(output_dir: Path, glyphs: list[BaseDrawing]):
    """
    Create horizontal and vertical arrays and save them to the provided path,
    in addition to an svg per individual drawing.
    """

    # write arrays
    array_h = PaddingDrawing.new(
        HArrayDrawing.new(glyphs, spacing=SPACING), padding=SPACING
    )
    array_v = PaddingDrawing.new(
        VArrayDrawing.new(glyphs, spacing=SPACING), padding=SPACING
    )

    array_h.export_svg(output_dir / "_array-h.svg")
    array_v.export_svg(output_dir / "_array-v.svg")

    if RASTER_SUPPORT:
        array_h.export_png(output_dir / "_array-h.png", scale=5)
        array_v.export_png(output_dir / "_array-v.png", scale=5)

    # write individual glyphs
    for drawing in glyphs:
        drawing.export_svg(output_dir)


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
