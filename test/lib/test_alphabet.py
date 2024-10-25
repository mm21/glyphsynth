from pathlib import Path

from glyphsynth.lib.alphabet.minimal import (
    letter_cls_list,
)

from ..conftest import write_glyphs


def test_letters(output_dir: Path):
    write_glyphs(output_dir, [letter_cls() for letter_cls in letter_cls_list])
