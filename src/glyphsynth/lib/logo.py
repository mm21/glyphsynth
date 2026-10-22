"""
Logo for GlyphSynth.
"""

from ..glyph.glyph import Glyph
from .alphabets.latin.runic import G, S


class GlyphSynthLogo(Glyph):
    def draw(self):
        self.draw_glyph(G)
        self.draw_glyph(S, scale=0.5)
