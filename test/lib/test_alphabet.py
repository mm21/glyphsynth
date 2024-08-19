from glyphsynth.lib.alphabet.minimal import (
    letter_cls_list,
)

from ..conftest import write_glyphs


def test_letters(output_dir: str):
    write_glyphs(output_dir, [letter_cls() for letter_cls in letter_cls_list])
