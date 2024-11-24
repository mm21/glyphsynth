import svgwrite.gradients

from .base import BaseElement

__all__ = [
    "BaseGradient",
    "LinearGradient",
    "RadialGradient",
]


class BaseGradient[GradientT: svgwrite.gradients._AbstractGradient](
    BaseElement[GradientT]
):
    def get_paint_server(self) -> str:
        return self._element.get_paint_server()


class LinearGradient(BaseGradient[svgwrite.gradients.LinearGradient]):
    _api_name = "linearGradient"


class RadialGradient(BaseGradient[svgwrite.gradients.RadialGradient]):
    _api_name = "radialGradient"
