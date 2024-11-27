from __future__ import annotations

from typing import Literal

from ._model import BaseFieldsModel

__all__ = [
    "Properties",
    "ShapeProperties",
    "GradientProperties",
]


class BasePropertiesModel(BaseFieldsModel):
    """
    Encapsulates graphics properties, as defined here:
    <https://www.w3.org/TR/SVG11/intro.html#TermProperty>

    And listed here: <https://www.w3.org/TR/SVG11/propidx.html>
    """


class ColorPropertiesMixin(BasePropertiesModel):
    """
    Common color-related properties.
    """

    color: str | None = None
    color_interpolation: Literal["auto", "sRGB", "linearRGB"] | None = None
    color_interpolation_filters: Literal[
        "auto", "sRGB", "linearRGB"
    ] | None = None
    color_profile: Literal[
        "auto", "sRGB"
    ] | str | None = None  # Can also be IRI
    color_rendering: Literal[
        "auto", "optimizeSpeed", "optimizeQuality"
    ] | None = None
    opacity: float | int | None = None


class PaintingPropertiesMixin(ColorPropertiesMixin, BasePropertiesModel):
    """
    Properties related to painting operations.
    """

    fill: str | None = None
    fill_opacity: float | int | None = None
    fill_rule: Literal["nonzero", "evenodd"] | None = None
    marker: str | None = None
    marker_end: str | None = None
    marker_mid: str | None = None
    marker_start: str | None = None
    stroke: str | None = None
    stroke_dasharray: str | None = None
    stroke_dashoffset: float | int | str | None = None
    stroke_linecap: Literal["butt", "round", "square"] | None = None
    stroke_linejoin: Literal["miter", "round", "bevel"] | None = None
    stroke_miterlimit: float | int | None = None
    stroke_opacity: float | int | None = None
    stroke_width: float | int | str | None = None
    shape_rendering: Literal[
        "auto", "optimizeSpeed", "crispEdges", "geometricPrecision"
    ] | None = None


class FontPropertiesMixin(BasePropertiesModel):
    """
    Properties related to font specification.
    """

    font: str | None = None
    font_family: str | None = None
    font_size: str | None = None  # Can be length or percentage
    font_size_adjust: Literal["none"] | float | int | None = None
    font_stretch: Literal[
        "normal",
        "wider",
        "narrower",
        "ultra-condensed",
        "extra-condensed",
        "condensed",
        "semi-condensed",
        "semi-expanded",
        "expanded",
        "extra-expanded",
        "ultra-expanded",
    ] | None = None
    font_style: Literal["normal", "italic", "oblique"] | None = None
    font_variant: Literal["normal", "small-caps"] | None = None
    font_weight: Literal[
        "normal", "bold", "bolder", "lighter"
    ] | int | None = None


class TextPropertiesMixin(ColorPropertiesMixin, BasePropertiesModel):
    """
    Properties related to text layout and rendering.
    """

    direction: Literal["ltr", "rtl"] | None = None
    letter_spacing: Literal[
        "normal"
    ] | str | None = None  # Can be "normal" or length
    text_decoration: Literal[
        "none", "underline", "overline", "line-through"
    ] | None = None
    unicode_bidi: Literal["normal", "embed", "bidi-override"] | None = None
    word_spacing: Literal[
        "normal"
    ] | str | None = None  # Can be "normal" or length
    writing_mode: Literal[
        "lr-tb", "rl-tb", "tb-rl", "lr", "rl", "tb"
    ] | None = None
    alignment_baseline: Literal[
        "auto",
        "baseline",
        "before-edge",
        "text-before-edge",
        "middle",
        "central",
        "after-edge",
        "text-after-edge",
        "ideographic",
        "alphabetic",
        "hanging",
        "mathematical",
    ] | None = None
    baseline_shift: str | None = None  # Can be length, percentage or keywords
    dominant_baseline: Literal[
        "auto",
        "use-script",
        "no-change",
        "reset-size",
        "ideographic",
        "alphabetic",
        "hanging",
        "mathematical",
        "central",
        "middle",
        "text-after-edge",
        "text-before-edge",
    ] | None = None
    text_anchor: Literal["start", "middle", "end"] | None = None
    text_rendering: Literal[
        "auto", "optimizeSpeed", "optimizeLegibility", "geometricPrecision"
    ] | None = None


class ImagePropertiesMixin(BasePropertiesModel):
    """
    Properties specific to image elements.
    """

    image_rendering: Literal[
        "auto", "optimizeSpeed", "optimizeQuality"
    ] | None = None
    preserve_aspect_ratio: str | None = (
        None  # Complex value with multiple parts
    )


class ClippingMaskingPropertiesMixin(BasePropertiesModel):
    """
    Properties related to clipping and masking.
    """

    clip: str | None = None
    clip_path: str | None = None
    clip_rule: Literal["nonzero", "evenodd"] | None = None
    mask: str | None = None


class GradientPropertiesMixin(ColorPropertiesMixin, BasePropertiesModel):
    """
    Properties specific to gradients.
    """

    stop_color: str | None = None
    stop_opacity: float | int | None = None


class FilterEffectPropertiesMixin(ColorPropertiesMixin, BasePropertiesModel):
    """
    Properties related to filter effects.
    """

    enable_background: Literal["accumulate", "new"] | None = None
    filter: str | None = None
    flood_color: str | None = None
    flood_opacity: float | int | None = None
    lighting_color: str | None = None


class CursorPropertiesMixin(BasePropertiesModel):
    """
    Properties related to cursors.
    """

    cursor: str | None = None  # Can be URI or keyword
    pointer_events: Literal[
        "visiblePainted",
        "visibleFill",
        "visibleStroke",
        "visible",
        "painted",
        "fill",
        "stroke",
        "all",
        "none",
    ] | None = None


class ViewportPropertiesMixin(BasePropertiesModel):
    """
    Properties related to the viewport.
    """

    overflow: Literal["visible", "hidden", "scroll", "auto"] | None = None
    display: Literal[
        "inline",
        "block",
        "list-item",
        "run-in",
        "compact",
        "marker",
        "table",
        "inline-table",
        "table-row-group",
        "table-header-group",
        "table-footer-group",
        "table-row",
        "table-column-group",
        "table-column",
        "table-cell",
        "table-caption",
        "none",
    ] | None = None
    visibility: Literal["visible", "hidden", "collapse"] | None = None


class Properties(
    PaintingPropertiesMixin,
    FontPropertiesMixin,
    TextPropertiesMixin,
    ClippingMaskingPropertiesMixin,
    GradientPropertiesMixin,
    FilterEffectPropertiesMixin,
    CursorPropertiesMixin,
    ViewportPropertiesMixin,
    BasePropertiesModel,
):
    """
    Class to represent all styling properties:
    <https://www.w3.org/TR/SVG11/styling.html#SVGStylingProperties>
    """

    def __init_subclass__(cls):
        super().__init_subclass__()

        valid_properties = Properties._get_fields()

        # ensure user didn't add any invalid properties
        for field in cls.model_fields.keys():
            assert field in valid_properties, f"{field} is not a valid property"


class ShapeProperties(
    PaintingPropertiesMixin,
    FilterEffectPropertiesMixin,
    CursorPropertiesMixin,
    ViewportPropertiesMixin,
    BasePropertiesModel,
):
    """
    Properties applicable to basic shapes.
    """


class GradientProperties(
    GradientPropertiesMixin,
    ColorPropertiesMixin,
):
    """
    Properties applicable to gradients.
    """
