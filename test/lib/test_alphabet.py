from pathlib import Path

from glyphsynth.lib.alphabets.latin.traditional import LETTER_CLASSES

from ..conftest import write_glyphs


def test_traditional(output_dir: Path):
    write_glyphs(output_dir, [letter_cls() for letter_cls in LETTER_CLASSES])
