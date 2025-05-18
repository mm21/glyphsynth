"""
Logo for GlyphSynth.
"""

from .alphabets.latin.runic import G, RunicLetterParams, S
from .letter import BaseLetterComboGlyph, LetterComboParams


class GlyphSynthLogo(BaseLetterComboGlyph[LetterComboParams]):
    def draw(self):
        self.draw_letter(G)
        self.draw_letter(
            S,
            params=RunicLetterParams(
                stroke_pct=self.params.letter_params.stroke_pct * 2
            ),
        ).scale(0.5, 0.5).translate(self.width / 2, self.height / 2)
