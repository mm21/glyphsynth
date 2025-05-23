from __future__ import annotations

from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any, Iterable, cast

import svgwrite.container
from pydantic import ConfigDict

from ._utils import extract_type_param
from .graphics._container import BaseGraphicsContainer
from .graphics._export import ExportContainer
from .graphics._model import BaseFieldsModel
from .graphics.elements._factory import ElementFactory
from .graphics.elements._mixins import PresentationMixin, TransformMixin
from .graphics.properties import Properties

__all__ = [
    "BaseParams",
    "BaseDrawing",
    "EmptyParams",
    "Drawing",
]


class BaseParams(BaseFieldsModel):
    """
    Subclass this class to create parameters for a Drawing.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    @property
    def desc(self) -> str:
        """
        Short, filename-friendly description of params and values.
        """

        def parse_val(val: Any) -> str:
            if isinstance(val, type):
                return val.__name__
            elif isinstance(val, BaseParams):
                return val.desc
            elif isinstance(val, Iterable) and not isinstance(val, str):
                return f"_".join([parse_val(v) for v in val])
            else:
                return str(val).replace("=", "~").replace(".", "_")

        params = []

        for field in type(self).model_fields.keys():
            val: Any = getattr(self, field)
            val_desc = parse_val(val)

            params.append(f"{field}-{val_desc}")

        return "__".join(params)


class BaseDrawing[ParamsT: BaseParams](
    ElementFactory,
    ExportContainer,
    BaseGraphicsContainer,
    TransformMixin,
    PresentationMixin,
    ABC,
):
    """
    Base class for a standalone or reusable drawing, sized in abstract
    (user) units.
    """

    params: ParamsT
    """
    Instance of params with type as specified by typevar.
    """

    default_params: ParamsT | None = None
    """
    Params to use as defaults for this drawing
    """

    _params_cls: type[ParamsT]
    """
    Params class: the type parameter provided as ParamsT, or EmptyParams
    if no type parameter provided.
    """

    _nested_glyphs: list[BaseDrawing]
    """
    List of glyphs nested under this one, mostly for debugging.
    """

    def __init__(
        self,
        *,
        drawing_id: str | None = None,
        params: ParamsT | None = None,
        properties: Properties | None = None,
        size: tuple[float | int, float | int] | None = None,
    ):
        """
        :param parent: Parent drawing, or `None`{l=python} to create top-level drawing
        :param drawing_id: Unique identifier, or `None`{l=python} to generate one
        """

        size_ = (float(size[0]), float(size[1])) if size else None
        super().__init__(drawing_id, properties, size_)

        self._nested_glyphs = []

        # set params
        params_cls = cast(ParamsT, type(self).get_params_cls())
        self.params = params_cls._aggregate(self.default_params, params)

        # invoke pre-init to setup needed state for user's init()
        self._pre_init()

        # invoke subclass's init (e.g. set properties based on params)
        self.init()

        # invoke post-init since canonical_size may be set in init()
        self._post_init()

        # invoke subclass's drawing logic
        self.draw()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(drawing_id={self.drawing_id})"

    def __init_subclass__(cls):
        """
        Populate _params_cls with the class representing the parameters for
        this drawing. If not subscripted with a type arg by the subclass,
        _params_cls is set to EmptyParams.
        """
        cls._params_cls = extract_type_param(cls, BaseParams) or EmptyParams

    @property
    def drawing_id(self) -> str | None:
        """
        A meaningful identifier to associate with this drawing. Also used as
        base name (without extension) of file to export when no filename is
        provided.
        """
        return self._id

    @cached_property
    def canonical_width(self) -> float:
        """
        Accessor for canonical width.
        """
        assert self.canonical_size
        return self.canonical_size[0]

    @cached_property
    def canonical_height(self) -> float:
        """
        Accessor for canonical height.
        """
        assert self.canonical_size
        return self.canonical_size[1]

    @cached_property
    def canonical_center(self) -> tuple[float, float]:
        """
        Accessor for canonical center.
        """
        return (self.canonical_width / 2, self.canonical_height / 2)

    @classmethod
    def get_params_cls(cls) -> type[ParamsT]:
        """
        Returns the {obj}`BaseParams` subclass with which this class is
        parameterized.
        """
        return cls._params_cls

    def init(self):
        ...

    def insert_drawing[
        DrawingT: BaseDrawing
    ](
        self,
        drawing: DrawingT,
        insert: tuple[float | int, float | int] | None = None,
    ) -> DrawingT:
        if insert:
            insert_norm = insert
        elif self.canonical_size is not None:
            # if insert not given, default to center of this drawing
            center = self.canonical_center
            insert_norm = (
                center[0] - drawing.width / 2,
                center[1] - drawing.height / 2,
            )
        else:
            insert_norm = None

        return super().insert_drawing(drawing, insert=insert_norm)

    @abstractmethod
    def draw(self):
        ...

    @property
    def _glyph(self) -> BaseDrawing:
        return self

    @property
    def _container(self) -> svgwrite.container.SVG:
        return self._svg

    def _pre_init(self):
        """
        Can be overridden by subclass for any init needed before user's init().
        """
        ...


class EmptyParams(BaseParams):
    pass


class Drawing(BaseDrawing[EmptyParams]):
    """
    Empty drawing to use as an on-the-fly alternative to subclassing
    {obj}`BaseDrawing`. It has an empty {obj}`BaseDrawing.draw`
    implementation; the user can then add graphics objects
    and other glyphs after creation.

    Example:

    ```python
    glyph1 = MyDrawing1()
    glyph2 = MyDrawing2()

    # create an empty drawing with unspecified size
    drawing = Drawing()

    # insert a drawing
    drawing.insert_drawing(glyph1)

    # insert another drawing in a different position
    drawing.insert_drawing(glyph2, (100, 100))
    ```
    """

    def draw(self):
        pass
