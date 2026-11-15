"""
Text elements.
"""

from __future__ import annotations

from typing import Literal

import svgwrite.text

from ..properties import TextProperties
from ._mixins import MaskingMixin, PresentationMixin, TransformMixin
from .base import BaseElement
from .paths import Path

__all__ = [
    "Text",
    "TSpan",
    "TextPath",
]


class _BaseTextContent[ElementT: svgwrite.text.TSpan](BaseElement[ElementT]):
    """
    Text content element which can hold nested spans.
    """

    def add_span(
        self,
        text: str,
        insert: tuple[float, float] | None = None,
        dx: float | None = None,
        dy: float | None = None,
        rotate: float | None = None,
        properties: TextProperties | None = None,
    ) -> TSpan:
        """
        Append a `<tspan>` to adjust position or properties of a run of text.

        :param text: Text content
        :param insert: Absolute position of span
        :param dx: Horizontal offset relative to the current text position
        :param dy: Vertical offset relative to the current text position
        :param rotate: Rotation of each glyph in degrees
        :param properties: Properties of span; inherits from parent otherwise
        """
        return TSpan(
            self._glyph_obj,
            self._element,
            text,
            insert=insert,
            dx=_listify(dx),
            dy=_listify(dy),
            rotate=_listify(rotate),
            **_get_values(properties),
        )


class Text(
    _BaseTextContent[svgwrite.text.Text],
    TransformMixin,
    PresentationMixin,
    MaskingMixin,
):
    """
    Wraps a `<text>` element.
    """

    _api_name = "text"

    def add_text_path(
        self,
        path: Path | str,
        text: str,
        start_offset: float | str | None = None,
        method: Literal["align", "stretch"] = "align",
        spacing: Literal["exact", "auto"] = "exact",
        properties: TextProperties | None = None,
    ) -> TextPath:
        """
        Append a `<textPath>` to render text along the given path.

        :param path: Path to follow, or IRI string (`"#id"`) of one
        :param text: Text content
        :param start_offset: Offset from start of path, as length or percentage
        :param method: Glyph rendering method
        :param spacing: Glyph spacing method
        :param properties: Properties of text; inherits from parent otherwise
        """
        return TextPath(
            self._glyph_obj,
            self._element,
            path._element if isinstance(path, Path) else path,
            text,
            startOffset=start_offset,
            method=method,
            spacing=spacing,
            **_get_values(properties),
        )


class TSpan(_BaseTextContent[svgwrite.text.TSpan], PresentationMixin):
    """
    Wraps a `<tspan>` element.
    """

    _api_name = "tspan"


class TextPath(BaseElement[svgwrite.text.TextPath], PresentationMixin):
    """
    Wraps a `<textPath>` element.
    """

    _api_name = "textPath"


def _listify(value: float | None) -> list[float] | None:
    return None if value is None else [value]


def _get_values(properties: TextProperties | None) -> dict[str, str]:
    if properties is None:
        return {}
    return {k: v for k, v in properties._get_values().items() if v is not None}
