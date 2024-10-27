from pathlib import Path
import logging
import os

from pytest import mark

from glyphsynth import RASTER_SUPPORT
from glyphsynth.lib import PaddingGlyph

from ..glyphs import ParentGlyph


def test_padding(output_dir: Path):
    glyph_inner = ParentGlyph()
    glyph = PaddingGlyph.new(glyph_inner)

    glyph.export_svg(output_dir)

    if RASTER_SUPPORT:
        glyph.export_png(output_dir)
    else:
        logging.warning("Skipping rasterizing")
