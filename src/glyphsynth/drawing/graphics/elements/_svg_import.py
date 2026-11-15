"""
Loading of externally-provided SVG documents.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

import svgwrite.base

__all__ = [
    "ROOT_SKIP",
    "RawElement",
    "parse",
    "get_size",
    "get_viewbox",
]

# attributes of the outermost <svg> which are consumed or meaningless on a <g>
ROOT_SKIP = {
    "width",
    "height",
    "viewBox",
    "x",
    "y",
    "id",
    "version",
    "baseProfile",
    "preserveAspectRatio",
    "zoomAndPan",
}

_SVG_NS = "http://www.w3.org/2000/svg"
_XLINK_NS = "http://www.w3.org/1999/xlink"
_XML_NS = "http://www.w3.org/XML/1998/namespace"

_PREFIXES = {_XLINK_NS: "xlink", _XML_NS: "xml"}


class RawElement(svgwrite.base.BaseElement):
    """
    Opaque `svgwrite` element which serializes a parsed XML subtree as-is.
    """

    def __init__(self, xml: ET.Element):
        super().__init__(debug=False)
        self.xml = xml
        self.elementname = xml.tag

    def get_xml(self) -> ET.Element:
        return self.xml


def parse(source: str | bytes | Path) -> ET.Element:
    """
    Parse source (path, or SVG markup as str/bytes) and return normalized `<svg>` root
    with namespaces removed from tags and attributes.
    """
    if isinstance(source, Path):
        root = ET.parse(source).getroot()
    elif isinstance(source, bytes):
        root = ET.fromstring(source)
    elif source.lstrip().startswith("<"):
        root = ET.fromstring(source)
    else:
        root = ET.parse(Path(source)).getroot()

    if _strip_ns(root.tag) != "svg":
        raise ValueError(f"Expected root <svg> element, got <{_strip_ns(root.tag)}>")

    _normalize(root)
    return root


def get_size(root: ET.Element) -> tuple[float, float] | None:
    viewbox = get_viewbox(root)
    width = _parse_length(root.get("width"))
    height = _parse_length(root.get("height"))

    if width is not None and height is not None:
        return (width, height)
    if viewbox is not None:
        return (viewbox[2], viewbox[3])
    return None


def get_viewbox(root: ET.Element) -> tuple[float, float, float, float] | None:
    value = root.get("viewBox")
    if value is None:
        return None
    parts = [float(p) for p in re.split(r"[\s,]+", value.strip()) if p]
    if len(parts) != 4:
        return None
    return (parts[0], parts[1], parts[2], parts[3])


def _normalize(elem: ET.Element):
    elem.tag = _strip_ns(elem.tag)
    elem.attrib = {_normalize_attr(k): v for k, v in elem.attrib.items()}
    for child in elem:
        _normalize(child)


def _strip_ns(name: str) -> str:
    # elements in the SVG namespace become plain tags; others are left as-is
    return name.removeprefix(f"{{{_SVG_NS}}}")


def _normalize_attr(name: str) -> str:
    if name.startswith("{"):
        ns, _, local = name[1:].partition("}")
        if ns in _PREFIXES:
            return f"{_PREFIXES[ns]}:{local}"
        return local
    return name


def _parse_length(value: str | None) -> float | None:
    """
    Parse length in user units; unitless and `px` only (relative units like `%` are not
    resolvable without context).
    """
    if value is None:
        return None
    match = re.fullmatch(
        r"\s*([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)\s*(px)?\s*", value
    )
    return float(match.group(1)) if match else None
