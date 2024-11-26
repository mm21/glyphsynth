from __future__ import annotations

from typing import TYPE_CHECKING

import svgwrite.container

from ._factory import ElementFactory
from ._mixins import PresentationMixin, TransformMixin
from .base import BaseElement

if TYPE_CHECKING:
    from ...glyph import BaseGlyph

__all__ = [
    "Group",
]


class Group(
    BaseElement[svgwrite.container.Group],
    TransformMixin,
    PresentationMixin,
    ElementFactory,
):
    _api_name = "g"

    @property
    def _glyph(self) -> BaseGlyph:
        return self._glyph_obj

    @property
    def _container(self) -> svgwrite.container.Group:
        return self._element
