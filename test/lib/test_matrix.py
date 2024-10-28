from pathlib import Path
from typing import Generator
import itertools

from glyphsynth.lib.matrix import MatrixParams, MatrixGlyph
from glyphsynth.lib.variants import BaseVariantExportFactory
from glyphsynth.lib.alphabet.minimal import (
    UNIT,
    LetterParams,
    BaseLetterGlyph,
    LetterComboParams,
    BaseLetterComboGlyph,
    A,
    M,
    T,
)

from ..conftest import write_glyph

LETTERS = [
    A,
    M,
    T,
]

COLORS = [
    "black",
    "red",
    "green",
    "blue",
]


class AMTComboParams(LetterComboParams):
    letter1: type[BaseLetterGlyph]
    letter2: type[BaseLetterGlyph]


class AMTComboGlyph(BaseLetterComboGlyph[AMTComboParams]):
    def draw(self):
        # draw letters given by params
        self.draw_letter(self.params.letter1)
        letter2 = self.draw_letter(self.params.letter2)

        # additionally rotate letter2
        letter2.rotate(180)


class VariantFactory(BaseVariantExportFactory[AMTComboGlyph]):
    MATRIX_WIDTH = len(COLORS)
    SPACING = UNIT / 10
    glyph_cls = AMTComboGlyph

    # generate variants of colors and letter combinations
    def get_params_variants(self) -> Generator[AMTComboParams, None, None]:
        for color, letter1, letter2 in itertools.product(
            COLORS, LETTERS, LETTERS
        ):
            yield AMTComboParams(
                letter_params=LetterParams(color=color),
                letter1=letter1,
                letter2=letter2,
            )


def test_matrix(output_dir: Path):
    rows: list[list[AMTComboGlyph]] = []

    for letter1, letter2 in itertools.product(LETTERS, LETTERS):
        row = []

        for color in COLORS:
            glyph = AMTComboGlyph(
                params=AMTComboParams(
                    letter_params=LetterParams(color=color),
                    letter1=letter1,
                    letter2=letter2,
                )
            )
            row.append(glyph)
        rows.append(row)

    matrix = MatrixGlyph.new(
        rows, glyph_id="amt-combo-matrix", spacing=UNIT / 10
    )
    write_glyph(output_dir, matrix)


def test_variants(output_dir: Path):
    for spec in VariantFactory():
        write_glyph(output_dir / spec.path, spec.glyph)