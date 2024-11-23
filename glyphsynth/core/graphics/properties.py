from __future__ import annotations

from typing import Self, cast

from pydantic import BaseModel

__all__ = [
    "PropertyValueType",
    "Properties",
    "ShapeProperties",
]

type PropertyValueType = str | None


class BasePropertiesModel(BaseModel):
    """
    Encapsulates graphics properties, as defined here:
    <https://www.w3.org/TR/SVG11/intro.html#TermProperty>

    And listed here: <https://www.w3.org/TR/SVG11/propidx.html>
    """

    @classmethod
    def _aggregate(cls, models: list[BasePropertiesModel]) -> Self:
        """
        Create a new model with values aggregated from provided models.
        """
        values: dict[str, str] = {}

        for model in models:
            values.update(model._get_values())

        return cls(**values)

    def _get_values(self) -> dict[str, str]:
        values: dict[str, str] = {}

        for field in list(self.model_fields.keys()):
            if (value := cast(str | None, getattr(self, field))) is not None:
                values[field] = value

        return values


class ColorPropertiesMixin(BasePropertiesModel):
    """
    Common color-related properties.
    """

    color: PropertyValueType = None
    color_interpolation: PropertyValueType = None
    color_interpolation_filters: PropertyValueType = None
    color_profile: PropertyValueType = None
    color_rendering: PropertyValueType = None
    opacity: PropertyValueType = None


class PaintingPropertiesMixin(ColorPropertiesMixin, BasePropertiesModel):
    """
    Properties related to painting operations.
    """

    fill: PropertyValueType = None
    fill_opacity: PropertyValueType = None
    fill_rule: PropertyValueType = None
    marker: PropertyValueType = None
    marker_end: PropertyValueType = None
    marker_mid: PropertyValueType = None
    marker_start: PropertyValueType = None
    stroke: PropertyValueType = None
    stroke_dasharray: PropertyValueType = None
    stroke_dashoffset: PropertyValueType = None
    stroke_linecap: PropertyValueType = None
    stroke_linejoin: PropertyValueType = None
    stroke_miterlimit: PropertyValueType = None
    stroke_opacity: PropertyValueType = None
    stroke_width: PropertyValueType = None
    shape_rendering: PropertyValueType = None


class FontPropertiesMixin(BasePropertiesModel):
    """
    Properties related to font specification.
    """

    font: PropertyValueType = None
    font_family: PropertyValueType = None
    font_size: PropertyValueType = None
    font_size_adjust: PropertyValueType = None
    font_stretch: PropertyValueType = None
    font_style: PropertyValueType = None
    font_variant: PropertyValueType = None
    font_weight: PropertyValueType = None


class TextPropertiesMixin(ColorPropertiesMixin, BasePropertiesModel):
    """
    Properties related to text layout and rendering.
    """

    direction: PropertyValueType = None
    letter_spacing: PropertyValueType = None
    text_decoration: PropertyValueType = None
    unicode_bidi: PropertyValueType = None
    word_spacing: PropertyValueType = None
    writing_mode: PropertyValueType = None
    alignment_baseline: PropertyValueType = None
    baseline_shift: PropertyValueType = None
    dominant_baseline: PropertyValueType = None
    glyph_orientation_horizontal: PropertyValueType = None
    glyph_orientation_vertical: PropertyValueType = None
    kerning: PropertyValueType = None
    text_anchor: PropertyValueType = None
    text_rendering: PropertyValueType = None


class ImagePropertiesMixin(BasePropertiesModel):
    """
    Properties specific to image elements.
    """

    # Specific to image rendering
    image_rendering: PropertyValueType = None
    preserve_aspect_ratio: PropertyValueType = None


class ClippingMaskingPropertiesMixin(BasePropertiesModel):
    """
    Properties related to clipping and masking.
    """

    clip: PropertyValueType = None
    clip_path: PropertyValueType = None
    clip_rule: PropertyValueType = None
    mask: PropertyValueType = None


class GradientPropertiesMixin(ColorPropertiesMixin, BasePropertiesModel):
    """
    Properties specific to gradients.
    """

    stop_color: PropertyValueType = None
    stop_opacity: PropertyValueType = None


class FilterEffectPropertiesMixin(ColorPropertiesMixin, BasePropertiesModel):
    """
    Properties related to filter effects.
    """

    enable_background: PropertyValueType = None
    filter: PropertyValueType = None
    flood_color: PropertyValueType = None
    flood_opacity: PropertyValueType = None
    lighting_color: PropertyValueType = None


class CursorPropertiesMixin(BasePropertiesModel):
    """
    Properties related to cursors.
    """

    cursor: PropertyValueType = None
    pointer_events: PropertyValueType = None


class ViewportPropertiesMixin(BasePropertiesModel):
    """
    Properties related to the viewport.
    """

    overflow: PropertyValueType = None
    display: PropertyValueType = None
    visibility: PropertyValueType = None


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

        valid_properties = Properties.model_fields.keys()

        # ensure user didn't add any invalid properties
        for field in cls.model_fields.keys():
            assert field in valid_properties, f"{field} is not a valid property"


class ShapeProperties(
    PaintingPropertiesMixin,
    FilterEffectPropertiesMixin,
    ViewportPropertiesMixin,
    CursorPropertiesMixin,
    BasePropertiesModel,
):
    """
    Properties applicable to basic shapes.
    """
