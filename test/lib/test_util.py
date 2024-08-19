import logging
import os

from pytest import mark

from glyphsynth import raster_support
from glyphsynth.lib import PaddingParams, PaddingGlyph

from ..conftest import ParentGlyph, UNIT


def test_padding(output_dir: str):
    glyph_inner = ParentGlyph()
    glyph = PaddingGlyph.new(glyph_inner)

    glyph.export_svg(output_dir)

    if raster_support:
        glyph.export_png(output_dir)
    else:
        logging.warning("Skipping rasterizing")
