import svgwrite.container

from .base import BaseElement
from .mixins import PresentationMixin, TransformMixin

__all__ = [
    "Group",
]


class Group(
    BaseElement[svgwrite.container.Group], TransformMixin, PresentationMixin
):
    _api_name = "g"

    def add(self, element: BaseElement):
        self._element.add(element._element)