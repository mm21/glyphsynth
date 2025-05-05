import itertools
from pathlib import Path
from typing import Generator

from glyphsynth.lib.alphabets.latin.traditional import (
    A,
    M,
    T,
    TraditionalLetterParams,
)
from glyphsynth.lib.letter import (
    UNIT,
    BaseLetterComboGlyph,
    BaseLetterGlyph,
    LetterComboParams,
)
from glyphsynth.lib.matrix import MatrixGlyph
from glyphsynth.lib.variants import BaseVariantExportFactory

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


class AMTVariantFactory(BaseVariantExportFactory[AMTComboGlyph]):
    MATRIX_WIDTH = len(COLORS)
    SPACING = UNIT / 10

    # generate variants of colors and letter combinations
    def get_params_variants(self) -> Generator[AMTComboParams, None, None]:
        for letter1, letter2, color in itertools.product(
            LETTERS, LETTERS, COLORS
        ):
            yield AMTComboParams(
                letter_params=TraditionalLetterParams(color=color),
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
                    letter_params=TraditionalLetterParams(color=color),
                    letter1=letter1,
                    letter2=letter2,
                )
            )
            row.append(glyph)
        rows.append(row)

    matrix = MatrixGlyph.new(
        rows, glyph_id="amt-combo-matrix", spacing=UNIT / 10, padding=UNIT / 10
    )
    write_glyph(output_dir, matrix)


def test_variants(output_dir: Path):
    for spec in AMTVariantFactory():
        write_glyph(output_dir / spec.path, spec.glyph)
