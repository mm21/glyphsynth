"""
"""
from __future__ import annotations

from typing import Callable, cast

import svgwrite.base
from svgwrite.container import SVG, Defs
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

    def __init__(
        self, drawing: Drawing, container: SVG | Defs, *args, **kwargs
    ):
        """
        Creates the corresponding `svgwrite` element, passing through
        extra kwargs. Should not be instantiated directly; use draw APIs.
        """
        api = getattr(drawing, self._api_name)
        self._element = cast(Callable[..., ElementT], api)(*args, **kwargs)
        self._mixin_obj = self._element
        container.add(self._element)

    @property
    def iri(self) -> str:
        return self._element.get_iri()

    @property
    def funciri(self) -> str:
        return self._element.get_funciri()
