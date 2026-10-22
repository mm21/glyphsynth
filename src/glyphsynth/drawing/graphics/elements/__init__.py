"""
Exports classes which encapsulate an SVG element.
"""

__submodules__ = [
    "base",
    "containers",
    "shapes",
    "gradients",
]

# isort: off
# <AUTOGEN_INIT>
from .base import (
    BaseElement,
)
from .containers import (
    Group,
)
from .shapes import (
    Line,
    Rect,
    Circle,
    Ellipse,
    Polyline,
    Polygon,
)
from .gradients import (
    BaseGradient,
    LinearGradient,
    RadialGradient,
    StopColor,
)

__all__ = [
    "BaseElement",
    "Group",
    "Line",
    "Rect",
    "Circle",
    "Ellipse",
    "Polyline",
    "Polygon",
    "BaseGradient",
    "LinearGradient",
    "RadialGradient",
    "StopColor",
]
# </AUTOGEN_INIT>
