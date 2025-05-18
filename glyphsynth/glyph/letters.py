"""
Helper for letter-based glyphs.
"""

import string

__all__ = [
    "LETTERS",
]

LETTERS: list[str] = [l for l in string.ascii_uppercase]
"""
List of letters A-Z.
"""
