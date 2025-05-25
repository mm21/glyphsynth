from pathlib import Path

from glyphsynth import MatrixDrawing
from glyphsynth.lib.alphabets.latin import runic, traditional

from ..conftest import write_drawing, write_drawings


def test_traditional(output_dir: Path):
    write_drawings(
        output_dir, [letter_cls() for letter_cls in traditional.LETTER_CLASSES]
    )


def test_runic(output_dir: Path):
    write_drawings(
        output_dir, [letter_cls() for letter_cls in runic.LETTER_CLASSES]
    )

    # generate 13x2 matrix for better viewing on mobile
    rows: list[list[runic.BaseRunicGlyph]] = []
    for i in range(len(runic.LETTER_CLASSES) // 2):
        letter1_cls, letter2_cls = runic.LETTER_CLASSES[i * 2 : i * 2 + 2]
        rows.append([letter1_cls(), letter2_cls()])

    matrix = MatrixDrawing.new(
        rows, drawing_id="runic-alphabet-vertical", spacing=10, padding=10
    )
    write_drawing(output_dir / "matrix", matrix, scale=2)
