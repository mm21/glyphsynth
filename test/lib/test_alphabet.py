from pathlib import Path

from glyphsynth.lib.alphabets.latin import runic, traditional

from ..conftest import write_drawings


def test_traditional(output_dir: Path):
    write_drawings(
        output_dir, [letter_cls() for letter_cls in traditional.LETTER_CLASSES]
    )


def test_runic(output_dir: Path):
    write_drawings(
        output_dir, [letter_cls() for letter_cls in runic.LETTER_CLASSES]
    )
