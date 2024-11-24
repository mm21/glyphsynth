"""
"""
from __future__ import annotations

from typing import Callable, cast

import svgwrite.base
from svgwrite.container import SVG
from svgwrite.drawing import Drawing

from .mixins import BaseMixin

__all__ = [
    "BaseElement",
]


class BaseElement[ElementT: svgwrite.base.BaseElement](BaseMixin):
    """
    Wraps an `svgwrite` SVG element and corresponding API mixins.
    """

    _api_name: str
    """
    Name of svgwrite API to invoke.
    """

    _element: ElementT

    def __init__(self, drawing: Drawing, svg: SVG, *args, **kwargs):
        """
        Creates the corresponding `svgwrite` element, passing through
        extra kwargs. Should not be instantiated directly; use draw APIs.
        """
        self._element = cast(
            Callable[..., ElementT], getattr(drawing, self._api_name)
        )(*args, **kwargs)
        self._mixin_obj = self._element
        svg.add(self._element)

    @property
    def iri(self) -> str:
        return self._element.get_iri()

    @property
    def funciri(self) -> str:
        return self._element.get_funciri()
