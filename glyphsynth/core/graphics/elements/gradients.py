from dataclasses import dataclass

import svgwrite.gradients

from .base import BaseElement

__all__ = [
    "BaseGradient",
    "LinearGradient",
    "RadialGradient",
    "StopColor",
]


@dataclass
class StopColor:
    color: str
    offset_pct: float
    opacity_pct: float | None = None


class BaseGradient[GradientT: svgwrite.gradients._AbstractGradient](
    BaseElement[GradientT]
):
    def get_paint_server(self) -> str:
        return self._element.get_paint_server()

    def add_colors(self, colors: list[str]):
        self._element.add_colors(colors)

    def add_stop_color(
        self, color: str, offset_pct: float, opacity_pct: float | None = None
    ):
        self._element.add_stop_color(
            color=color, offset=offset_pct / 100, opacity=opacity_pct / 100
        )

    def add_stop_colors(self, stop_colors: list[StopColor]):
        for stop in stop_colors:
            self.add_stop_color(
                stop.color, stop.offset_pct, opacity_pct=stop.opacity_pct
            )

    def _configure(
        self, colors: list[str] | None, stop_colors: list[StopColor] | None
    ):
        assert colors or stop_colors, f"No stop configurations passed"
        assert not (
            colors and stop_colors
        ), f"Multiple stop configurations passed: colors={colors}, stop_colors={stop_colors}"

        if colors:
            self.add_colors(colors)
        elif stop_colors:
            self.add_stop_colors(stop_colors)


class LinearGradient(BaseGradient[svgwrite.gradients.LinearGradient]):
    _api_name = "linearGradient"


class RadialGradient(BaseGradient[svgwrite.gradients.RadialGradient]):
    _api_name = "radialGradient"
