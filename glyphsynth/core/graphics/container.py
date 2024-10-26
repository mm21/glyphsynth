from __future__ import annotations

import logging
from typing import Any, cast

from svgwrite.drawing import Drawing
from svgwrite.container import SVG, Group

from .properties import Properties


__all__ = []


class BaseContainer:
    """
    Container for drawing and manipulation of low-level graphics objects.

    There are 2 SVG trees maintained:
    1. Standalone glyph
        drawing (root <svg>)
            wrapper svg (if size provided)
                canonical svg
    2. Placement in parent glyph
        svg-parent
            svg-wrapper-placement (insert only)
                group (w/transforms, e.g. rotation)
                    svg-wrapper-scaling (width/height/viewbox only)
                        svg-canonical
    """

    DefaultProperties: type[Properties] = Properties
    """
    Subclass of Properties with properties set as class attributes.
    
    May be subclassed in-place or assigned to an existing subclass.
    For example, subclassing in-place:

    ```python
    class MyGlyph(BaseGlyph):

        class DefaultProperties(Properties):
            color: PropertyValue = "black"
            stroke_width: PropertyValue = "10"
        
        ...
    ```
    """

    properties: Properties
    """
    Properties automatically propagated to graphics objects in draw_*() APIs.
    """

    size_canon: tuple[float, float] | None = None
    """
    Canonical size in user units, as provided by concrete class either as class
    attribute or upon creation in {obj}`BaseGlyph.init`.

    Used to set a consistent size for drawing, invariant of the size 
    passed upon instantiation.

    May be `None`, in which case {obj}`BaseContainer.size`, 
    {obj}`BaseContainer.width`, and {obj}`BaseContainer.height`
    will return `None`.

    Note that some {obj}`BaseGlyph` subclasses may require that 
    this field is not `None`.
    """

    viewbox_canon: tuple[tuple[float, float], tuple[float, float]] | None = None

    _id: str | None
    """
    Unique id for this container.
    """

    _size: tuple[float, float] | None = None
    """
    Instantiated size, set upon glyph creation. If `None`, not rescaled;
    uses canonical size.
    """

    _drawing: Drawing
    """
    Drawing object, unique to each Glyph.
    """

    _svg: SVG
    """
    Canonical SVG container for all elements generated by this glyph.
    """

    _group: Group
    """
    Group to hold wrapper SVG container when added to a parent glyph.
    Transformations are performed on this group rather than the <svg> itself
    as <svg> does not support transformations in SVG 1.1.
    """

    _nested_glyphs: list[BaseContainer] = []
    """
    List of glyphs nested under this one, mostly for debugging.
    """

    def __init__(
        self,
        id_: str | None,
        properties: Properties | None,
        size: tuple[float, float] | None,
    ):
        self._id = id_
        self._size = size
        self._drawing = Drawing()
        self._group = self._drawing.g(**self._get_elem_kwargs(suffix="group"))
        self._nested_glyphs = []

        self.properties = (
            self.DefaultProperties() if properties is None else properties
        )

    @property
    def has_size(self) -> bool:
        try:
            _ = self.size
        except AssertionError:
            return False

        return True

    # TODO: document: raises exception + add custom exception
    @property
    def size(self) -> tuple[float, float]:
        s = self._size or self.size_canon
        assert s is not None
        return s

    @property
    def width(self) -> float:
        return self.size[0]

    @property
    def height(self) -> float:
        return self.size[1]

    @property
    def _id_norm(self) -> str:
        return self._id or type(self).__name__

    def _get_elem_kwargs(self, suffix: str | None = None) -> dict[str, str]:
        kwargs: dict[str, str] = {}
        suffix_ = "" if suffix is None else f"-{suffix}"

        if self._id:
            kwargs["id_"] = f"{self._id}{suffix_}"

        kwargs["class_"] = f"{type(self).__name__}{suffix_}"

        return kwargs

    def _init_post(self):
        # create canonical svg
        self._svg = cast(
            SVG,
            self._drawing.svg(
                **self._get_elem_kwargs(),
                size=self.size_canon,
            ),
        )

        # set viewbox, if configured
        if self.viewbox_canon is not None:
            x, y = self.viewbox_canon[0]
            w, h = self.viewbox_canon[1]
            self._svg.viewbox(x, y, w, h)
            self._svg.fit()

        # add to drawing for standalone glyph
        if self._size is None:
            # no scaling needed, add svg directly
            self._drawing.add(self._svg)
            self._group.add(self._svg)
        else:
            # create wrapper svg and rescale
            svg_wrapper: SVG = self._create_wrapper_scale()
            self._drawing.add(svg_wrapper)
            self._group.add(svg_wrapper)

        # set top-level dimensions explicitly as larger SVGs
        # are unexpectedly truncated when sized to 100% (default)
        if self.has_size:
            self._drawing["width"] = str(self.size[0])
            self._drawing["height"] = str(self.size[1])

    def _create_wrapper_scale(self) -> SVG:
        """
        Create SVG wrapper for canonical SVG object to handle
        placement/scaling.
        """

        size_kwargs = {} if self._size is None else {"size": self._size}
        wrapper_scale = cast(
            SVG,
            self._drawing.svg(
                **self._get_elem_kwargs(suffix="wrapper-scale"),
                **size_kwargs,
            ),
        )
        self._rescale_svg(wrapper_scale, self._size)
        wrapper_scale.add(self._svg)

        return wrapper_scale

    def _rescale_svg(
        self,
        svg: SVG,
        size: tuple[float, float] | tuple[str, str] | None,
        set_size: bool = False,
    ):
        if size is not None:
            if set_size:
                svg["width"] = str(size[0])
                svg["height"] = str(size[1])

            if self.size_canon is None:
                logging.warning(
                    f"Rescaling glyph {self} which has no canonical size; viewbox will not be set, so results may be unexpected"
                )
            else:
                svg.viewbox(
                    0, 0, round(self.size_canon[0]), round(self.size_canon[1])
                )
                svg.fit()
