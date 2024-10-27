from pathlib import Path
from typing import Generator
import itertools

from glyphsynth.lib.variants import BaseVariantExportFactory
from glyphsynth.lib.alphabet.minimal import (
    LETTER_CLS_LIST,
    UNIT,
    BaseLetterGlyph,
    LetterComboParams,
    BaseLetterComboGlyph,
    A,
    M,
    T,
)

from ..conftest import write_glyph, write_glyphs

LETTERS_TEST = [
    A,
    M,
    T,
]


class ParamsTest(LetterComboParams):
    letters: list[type[BaseLetterGlyph]]

    @property
    def desc(self) -> str:
        """
        Override to create valid glyph_id.
        """
        return f"{'_'.join([l.__name__ for l in self.letters])}"


class GlyphTest[ParamsT: ParamsTest](BaseLetterComboGlyph[ParamsT]):
    def draw(self):
        for letter_cls in self.params.letters:
            self.draw_letter(letter_cls)


class VariantFactoryTest(BaseVariantExportFactory[GlyphTest]):
    MATRIX_WIDTH = len(LETTERS_TEST)
    SPACING = UNIT / 10
    glyph_cls = GlyphTest

    def get_params_variants(self) -> Generator[ParamsTest, None, None]:
        for letter1, letter2, letter3 in itertools.product(
            LETTERS_TEST, LETTERS_TEST, LETTERS_TEST
        ):
            yield ParamsTest(letters=[letter1, letter2, letter3])


def test_letters(output_dir: Path):
    write_glyphs(output_dir, [letter_cls() for letter_cls in LETTER_CLS_LIST])


def test_variants(output_dir: Path):
    for spec in VariantFactoryTest():
        write_glyph(output_dir / spec.path, spec.glyph)
