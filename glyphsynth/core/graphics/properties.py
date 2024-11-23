from __future__ import annotations

from pydantic import BaseModel

__all__ = [
    "Properties",
    "PaintingProperties",
    "FontProperties",
    "PropertyValue",
]

type PropertyValue = str | None


class BaseProperties(BaseModel):
    """
    Encapsulates graphics properties, as defined here:
    <https://www.w3.org/TR/SVG11/intro.html#TermProperty>

    And listed here: <https://www.w3.org/TR/SVG11/propidx.html>
    """


class PaintingProperties(BaseProperties):
    color: PropertyValue = None
    color_interpolation: PropertyValue = None
    color_interpolation_filters: PropertyValue = None
    color_profile: PropertyValue = None
    color_rendering: PropertyValue = None
    fill: PropertyValue = None
    fill_opacity: PropertyValue = None
    fill_rule: PropertyValue = None
    image_rendering: PropertyValue = None
    marker: PropertyValue = None
    marker_end: PropertyValue = None
    marker_mid: PropertyValue = None
    marker_start: PropertyValue = None
    shape_rendering: PropertyValue = None
    stroke: PropertyValue = None
    stroke_dasharray: PropertyValue = None
    stroke_dashoffset: PropertyValue = None
    stroke_linecap: PropertyValue = None
    stroke_linejoin: PropertyValue = None
    stroke_miterlimit: PropertyValue = None
    stroke_opacity: PropertyValue = None
    stroke_width: PropertyValue = None
    text_rendering: PropertyValue = None


class FontProperties(BaseProperties):
    font: PropertyValue = None
    font_family: PropertyValue = None
    font_size: PropertyValue = None
    font_size_adjust: PropertyValue = None
    font_stretch: PropertyValue = None
    font_style: PropertyValue = None
    font_variant: PropertyValue = None
    font_weight: PropertyValue = None


class Properties(PaintingProperties, FontProperties):
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
