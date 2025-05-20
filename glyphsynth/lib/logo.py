"""
Logo for GlyphSynth.
"""

from ..glyph.glyph import Glyph, GlyphParams
from .alphabets.latin.runic import G, S


class GlyphSynthLogo(Glyph):
    def draw(self):
        self.draw_glyph(G)
        self.draw_glyph(
            S,
            params=GlyphParams(stroke_pct=self.params.stroke_pct * 2),
        ).scale(0.5, 0.5).translate(self.width / 2, self.height / 2)
