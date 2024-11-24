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
    pass


class LinearGradient(BaseGradient[svgwrite.gradients.LinearGradient]):
    _api_name = "linearGradient"


class RadialGradient(BaseGradient[svgwrite.gradients.RadialGradient]):
    _api_name = "radialGradient"