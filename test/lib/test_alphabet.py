from pathlib import Path

from glyphsynth.lib.alphabet.minimal import (
    LETTER_CLS_LIST,
)

from ..conftest import write_glyphs


def test_letters(output_dir: Path):
    write_glyphs(output_dir, [letter_cls() for letter_cls in LETTER_CLS_LIST])
