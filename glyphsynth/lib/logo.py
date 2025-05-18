"""
Logo for GlyphSynth.
"""

from .alphabets.latin.runic import G, S
from .letter import BaseLetterComboGlyph


class GlyphSynthLogo(BaseLetterComboGlyph):
    def draw(self):
        self.draw_letter(G)
        self.draw_letter(S)
        # self.draw_letter(S).rotate(90)
