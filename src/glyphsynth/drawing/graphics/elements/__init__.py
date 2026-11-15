"""
Exports classes which encapsulate an SVG element.
"""

__submodules__ = [
    "base",
    "containers",
    "shapes",
    "paths",
    "text",
    "image",
    "gradients",
]

# isort: off
# <AUTOGEN_INIT>
from .base import (
    BaseElement,
)
from .containers import (
    BaseContainer,
    Group,
    Symbol,
    Marker,
    Pattern,
    ClipPath,
    Mask,
    Use,
)
from .shapes import (
    Line,
    Rect,
    Circle,
    Ellipse,
    Polyline,
    Polygon,
)
from .paths import (
    Path,
)
from .text import (
    Text,
    TSpan,
    TextPath,
)
from .image import (
    Image,
)
from .gradients import (
    BaseGradient,
    LinearGradient,
    RadialGradient,
    StopColor,
)

__all__ = [
    "BaseElement",
    "BaseContainer",
    "Group",
    "Symbol",
    "Marker",
    "Pattern",
    "ClipPath",
    "Mask",
    "Use",
    "Line",
    "Rect",
    "Circle",
    "Ellipse",
    "Polyline",
    "Polygon",
    "Path",
    "Text",
    "TSpan",
    "TextPath",
    "Image",
    "BaseGradient",
    "LinearGradient",
    "RadialGradient",
    "StopColor",
]
# </AUTOGEN_INIT>
