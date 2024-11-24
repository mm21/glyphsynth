"""
"""

from typing import Callable

from svgwrite.base import BaseElement
from svgwrite.drawing import Drawing


class BaseElementContainer[ElementT: BaseElement]:
    _api_name: str
    """
    Name of svgwrite API to invoke.
    """

    _element: ElementT

    def __init__(self, drawing: Drawing, *args, **kwargs):
        """
        Creates the corresponding `svgwrite` element, passing through
        extra kwargs. Should not be instantiated directly; use draw APIs.
        """
        draw_api: Callable[..., BaseElement] = getattr(drawing, self._api_name)
        self._element = draw_api(*args, **kwargs)
