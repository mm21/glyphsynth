from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path as FilePath
from typing import TYPE_CHECKING, Literal

import svgwrite.base
import svgwrite.container

from .._model import BaseFieldsModel
from ..properties import ShapeProperties, TextProperties
from ._svg_import import ROOT_SKIP, RawElement, get_size, get_viewbox, parse
from .base import BaseElement
from .gradients import LinearGradient, RadialGradient, StopColor
from .image import Image
from .paths import Path
from .shapes import Circle, Ellipse, Line, Polygon, Polyline, Rect
from .text import Text

if TYPE_CHECKING:
    from ...drawing import BaseDrawing
    from .containers import (
        ClipPath,
        Group,
        ImportedSvg,
        Marker,
        Mask,
        Pattern,
        Symbol,
        Use,
    )

type _Units = Literal["userSpaceOnUse", "objectBoundingBox"]

__all__ = [
    "ElementFactory",
]


class ElementFactory(ABC):
    @property
    @abstractmethod
    def _glyph(self) -> BaseDrawing: ...

    @property
    @abstractmethod
    def _container(self) -> svgwrite.base.BaseElement: ...

    def draw_line(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        properties: ShapeProperties | None = None,
    ) -> Line:
        return Line(
            self._glyph,
            self._container,
            start=start,
            end=end,
            **self._get_extra(properties),
        )

    def draw_polyline(
        self,
        points: Iterable[tuple[float, float]],
        properties: ShapeProperties | None = None,
    ) -> Polyline:
        return Polyline(
            self._glyph,
            self._container,
            points=[p for p in points],
            **self._get_extra(properties),
        )

    def draw_polygon(
        self,
        points: Iterable[tuple[float, float]],
        properties: ShapeProperties | None = None,
    ) -> Polygon:
        return Polygon(
            self._glyph,
            self._container,
            points=[p for p in points],
            **self._get_extra(properties),
        )

    def draw_rect(
        self,
        insert: tuple[float, float],
        size: tuple[float, float],
        radius_x: float | None = None,
        radius_y: float | None = None,
        properties: ShapeProperties | None = None,
    ) -> Rect:
        return Rect(
            self._glyph,
            self._container,
            insert=insert,
            size=size,
            rx=radius_x,
            ry=radius_y,
            **self._get_extra(properties),
        )

    def draw_circle(
        self,
        center: tuple[float, float],
        radius: float,
        properties: ShapeProperties | None = None,
    ) -> Circle:
        return Circle(
            self._glyph,
            self._container,
            center=center,
            r=radius,
            **self._get_extra(properties),
        )

    def draw_ellipse(
        self,
        center: tuple[float, float],
        radius: tuple[float, float],
        properties: ShapeProperties | None = None,
    ) -> Ellipse:
        return Ellipse(
            self._glyph,
            self._container,
            center=center,
            r=radius,
            **self._get_extra(properties),
        )

    def draw_path(
        self,
        start: tuple[float, float] | None = None,
        properties: ShapeProperties | None = None,
    ) -> Path:
        """
        Draw a path, optionally starting at the given point. Add commands using the
        returned {obj}`Path`'s methods.
        """
        path = Path(self._glyph, self._container, **self._get_extra(properties))
        if start is not None:
            path.move_to(start)
        return path

    def draw_arc(
        self,
        center: tuple[float, float],
        radius: float | tuple[float, float],
        start_angle: float,
        end_angle: float,
        properties: ShapeProperties | None = None,
    ) -> Path:
        """
        Draw an arc of a circle or axis-aligned ellipse. Angles are in degrees, measured
        clockwise from the positive x-axis; the arc is drawn clockwise if
        `end_angle > start_angle` and counterclockwise otherwise.

        :param center: Center of circle/ellipse
        :param radius: Radius as a single value for a circular arc, or `(rx, ry)`
        :param start_angle: Start angle in degrees
        :param end_angle: End angle in degrees
        """
        return self.draw_path(properties=properties).arc(
            center, radius, start_angle, end_angle
        )

    def draw_text(
        self,
        text: str = "",
        insert: tuple[float, float] | None = None,
        properties: TextProperties | None = None,
    ) -> Text:
        """
        Draw text. Add spans or text along a path using the returned {obj}`Text`'s
        methods.

        :param text: Text content
        :param insert: Position of the text's anchor point on its baseline
        """
        return Text(
            self._glyph,
            self._container,
            text,
            insert=insert,
            **self._get_extra(properties, TextProperties),
        )

    def draw_image(
        self,
        href: str,
        insert: tuple[float, float] | None = None,
        size: tuple[float, float] | None = None,
    ) -> Image:
        """
        Draw an image.

        :param href: URL or data URI of image
        :param insert: Position of top-left corner
        :param size: Size of image's viewport
        """
        return Image(self._glyph, self._container, href, insert=insert, size=size)

    def draw_use(
        self,
        element: BaseElement | str,
        insert: tuple[float, float] | None = None,
        size: tuple[float, float] | None = None,
        properties: ShapeProperties | None = None,
    ) -> Use:
        """
        Draw an instance of another element, such as a {obj}`Symbol`.

        :param element: Element to instantiate, or IRI string (`"#id"`) of one
        :param insert: Position at which to place element
        :param size: Size of viewport; applicable to referenced symbols
        :param properties: Properties inherited by referenced element
        """
        from .containers import Use

        return Use(
            self._glyph,
            self._container,
            element._element if isinstance(element, BaseElement) else element,
            insert=insert,
            size=size,
            **_get_explicit(properties),
        )

    def create_group(self, properties: ShapeProperties | None = None) -> Group:
        from .containers import Group

        # only use passed properties instead of inheriting from drawing
        return Group(self._glyph, self._container, **_get_explicit(properties))

    def load_svg(
        self,
        source: str | bytes | FilePath,
        properties: ShapeProperties | None = None,
    ) -> ImportedSvg:
        """
        Load an externally-provided SVG and add it to this container. The outermost
        `<svg>` element is stripped and its contents placed in a group, so the whole
        image can be manipulated together (translate, rotate, scale, fill, etc.).

        The group is positioned such that the SVG's `viewBox` origin is at (0, 0), and
        scaled to its `width`/`height` if both are given and differ from the `viewBox`
        size. Presentation attributes on the outermost `<svg>` (e.g. `fill`, `style`)
        are kept on the group.

        Note ids within the SVG are preserved and so may collide with other ids in the
        drawing.

        :param source: Path to an SVG file, or SVG markup as `str` or `bytes`
        :param properties: Properties set on the group
        :raises ValueError: If the document's root element is not `<svg>`
        """
        from .containers import ImportedSvg

        root = parse(source)
        group = ImportedSvg(self._glyph, self._container, **_get_explicit(properties))

        for key, value in root.attrib.items():
            if key not in ROOT_SKIP and not key.startswith("xmlns"):
                group._element.attribs.setdefault(key, value)

        size = get_size(root)
        viewbox = get_viewbox(root)
        group.size = size
        group.original_viewbox = viewbox

        # normalization is applied on an inner group so any transforms subsequently
        # applied to the returned group are in terms of the SVG's size
        inner = self._glyph._drawing.g()
        group._element.add(inner)

        if viewbox is not None:
            min_x, min_y, vb_width, vb_height = viewbox
            if size is not None and vb_width and vb_height:
                scale_x, scale_y = size[0] / vb_width, size[1] / vb_height
                if (scale_x, scale_y) != (1, 1):
                    inner.scale(scale_x, scale_y)
            if (min_x, min_y) != (0, 0):
                inner.translate(-min_x, -min_y)

        for child in root:
            inner.add(RawElement(child))

        return group

    def create_symbol(self, properties: ShapeProperties | None = None) -> Symbol:
        """
        Create a symbol: a template which is only rendered via
        {obj}`ElementFactory.draw_use`. Typically given a viewbox using
        {obj}`Symbol.viewbox`.
        """
        from .containers import Symbol

        return Symbol(self._glyph, self._glyph._svg.defs, **_get_explicit(properties))

    def create_marker(
        self,
        size: tuple[float, float],
        ref: tuple[float, float] | None = None,
        orient: Literal["auto", "auto-start-reverse"] | float | None = "auto",
        units: Literal["strokeWidth", "userSpaceOnUse"] | None = None,
        properties: ShapeProperties | None = None,
    ) -> Marker:
        """
        Create a marker to draw at vertices of shapes using `markers()`.

        :param size: Size of marker viewport
        :param ref: Point in marker's coordinates aligned to the vertex
        :param orient: Rotation of marker: `"auto"` to align with path direction,
            or angle in degrees
        :param units: Coordinate system of `size`; defaults to `"strokeWidth"`,
            scaling the marker with the stroke width
        """
        from .containers import Marker

        extra = _get_explicit(properties)
        if units is not None:
            extra["markerUnits"] = units

        return Marker(
            self._glyph,
            self._glyph._svg.defs,
            insert=ref,
            size=size,
            orient=orient,
            **extra,
        )

    def create_pattern(
        self,
        size: tuple[float, float],
        insert: tuple[float, float] | None = None,
        units: _Units = "userSpaceOnUse",
        content_units: _Units | None = None,
        inherit: str | BaseElement | None = None,
    ) -> Pattern:
        """
        Create a tiled pattern to use with `fill(pattern=...)` or `stroke(pattern=...)`.

        :param size: Size of each tile
        :param insert: Offset of tiles
        :param units: Coordinate system of `size` and `insert`
        :param content_units: Coordinate system of pattern contents
        :param inherit: Pattern to inherit attributes and contents from
        """
        from .containers import Pattern

        extra: dict[str, str] = {"patternUnits": units}
        if content_units is not None:
            extra["patternContentUnits"] = content_units

        return Pattern(
            self._glyph,
            self._glyph._svg.defs,
            insert=insert,
            size=size,
            inherit=_normalize_inherit(inherit),
            **extra,
        )

    def create_clip_path(self, units: _Units | None = None) -> ClipPath:
        """
        Create a clip path to use with `clip_path()`.

        :param units: Coordinate system of contents; defaults to `"userSpaceOnUse"`
        """
        from .containers import ClipPath

        extra = {"clipPathUnits": units} if units is not None else {}
        return ClipPath(self._glyph, self._glyph._svg.defs, **extra)

    def create_mask(
        self,
        insert: tuple[float, float] | None = None,
        size: tuple[float, float] | None = None,
        units: _Units | None = None,
        content_units: _Units | None = None,
    ) -> Mask:
        """
        Create a mask to use with `mask()`. The luminance of its contents is used as
        alpha: white is opaque, black is transparent.

        :param insert: Top-left corner of mask region
        :param size: Size of mask region
        :param units: Coordinate system of `insert` and `size`; defaults to
            `"objectBoundingBox"`
        :param content_units: Coordinate system of contents; defaults to
            `"userSpaceOnUse"`
        """
        from .containers import Mask

        extra: dict[str, str] = {}
        if units is not None:
            extra["maskUnits"] = units
        if content_units is not None:
            extra["maskContentUnits"] = content_units

        return Mask(
            self._glyph, self._glyph._svg.defs, start=insert, size=size, **extra
        )

    def create_linear_gradient(
        self,
        start: tuple[float, float] | None = None,
        end: tuple[float, float] | None = None,
        colors: list[str] | list[StopColor] | None = None,
        inherit: str | BaseElement | None = None,
    ) -> LinearGradient:
        gradient = LinearGradient(
            self._glyph,
            self._glyph._svg.defs,
            start=start,
            end=end,
            inherit=_normalize_inherit(inherit),
            gradientUnits="userSpaceOnUse",
        )
        gradient._configure(colors)
        return gradient

    def create_radial_gradient(
        self,
        center: tuple[float, float] | None = None,
        radius: float | None = None,
        focal: tuple[float, float] | None = None,
        colors: list[str] | list[StopColor] | None = None,
        inherit: str | BaseElement | None = None,
    ) -> RadialGradient:
        gradient = RadialGradient(
            self._glyph,
            self._glyph._svg.defs,
            center=center,
            r=radius,
            focal=focal,
            inherit=_normalize_inherit(inherit),
            gradientUnits="userSpaceOnUse",
        )
        gradient._configure(colors)
        return gradient

    # TODO: if drawing has drawing_id, add to defs (if not present) and insert <use>
    def insert_drawing[DrawingT: BaseDrawing](
        self,
        drawing: DrawingT,
        insert: tuple[float | int, float | int] | None = None,
    ) -> DrawingT:
        self._glyph._nested_glyphs.append(drawing)

        # add group to self, using wrapper svg for placement
        wrapper_insert: svgwrite.container.SVG = self._glyph._drawing.svg(
            **drawing._get_elem_kwargs(suffix="wrapper-insert"),
            insert=insert,
        )

        wrapper_insert.add(drawing._group)
        self._container.add(wrapper_insert)

        return drawing

    def _get_extra(
        self,
        properties: BaseFieldsModel | None,
        properties_cls: type[BaseFieldsModel] = ShapeProperties,
    ) -> dict[str, str]:
        """
        Get extra kwargs to pass to svgwrite APIs.
        """
        # override defaults from the drawing with given properties
        props = properties_cls._aggregate(
            self._glyph.properties,
            properties,
        )

        # get values as dict
        values = props._get_values()

        # filter out unset values
        return {k: v for k, v in values.items() if v is not None}


def _get_explicit(properties: BaseFieldsModel | None) -> dict[str, str]:
    """
    Get kwargs from only the given properties, not inheriting from the drawing.
    """
    if properties is None:
        return {}
    return {k: v for k, v in properties._get_values().items() if v is not None}


def _normalize_inherit(inherit: str | BaseElement | None) -> str | None:
    if isinstance(inherit, BaseElement):
        return inherit.iri
    return inherit
