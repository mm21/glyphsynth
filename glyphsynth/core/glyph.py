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
    "BaseGlyph",
    "EmptyParams",
    "EmptyGlyph",
]


class BaseParams(BaseFieldsModel):
    """
    Subclass this class to create parameters for a Glyph.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

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


class BaseGlyph[ParamsT: BaseParams](
    ElementFactory,
    ExportContainer,
    BaseGraphicsContainer,
    TransformMixin,
    PresentationMixin,
    ABC,
):
    """
    Base class for a standalone or reusable glyph, sized in abstract
    (user) units.
    """

    params: ParamsT
    """
    Instance of params with type as specified by typevar.
    """

    default_params: ParamsT | None = None
    """
    Params to use as defaults for this glyph
    """

    _params_cls: type[ParamsT]
    """
    Params class: the type parameter provided as ParamsT, or EmptyParams
    if no type parameter provided.
    """

    _nested_glyphs: list[BaseGlyph]
    """
    List of glyphs nested under this one, mostly for debugging.
    """

    def __init__(
        self,
        *,
        glyph_id: str | None = None,
        params: ParamsT | None = None,
        properties: Properties | None = None,
        size: tuple[float | int, float | int] | None = None,
    ):
        """
        :param parent: Parent glyph, or `None`{l=python} to create top-level glyph
        :param glyph_id: Unique identifier, or `None`{l=python} to generate one
        """

        size_ = (float(size[0]), float(size[1])) if size else None
        super().__init__(glyph_id, properties, size_)

        self._nested_glyphs = []

        # set params
        params_cls = cast(ParamsT, type(self).get_params_cls())
        self.params = params_cls._aggregate(self.default_params, params)

        # invoke subclass's init (e.g. set properties based on params)
        self.init()

        # invoke post-init since canonical_size may be set in init()
        self._init_post()

        # invoke subclass's drawing logic
        self.draw()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(glyph_id={self.glyph_id})"

    def __init_subclass__(cls):
        """
        Populate _params_cls with the class representing the parameters for
        this glyph. If not subscripted with a type arg by the subclass,
        _params_cls is set to EmptyParams.
        """
        cls._params_cls = extract_type_param(cls, BaseParams) or EmptyParams

    @property
    def glyph_id(self) -> str | None:
        """
        A meaningful identifier to associate with this glyph. Also used as
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

    def insert_glyph[
        GlyphT: BaseGlyph
    ](
        self,
        glyph: GlyphT,
        insert: tuple[float | int, float | int] | None = None,
    ) -> GlyphT:
        if insert:
            insert_norm = insert
        elif self.canonical_size is not None:
            # if insert not given, default to center of this glyph
            center = self.canonical_center
            insert_norm = (
                center[0] - glyph.width / 2,
                center[1] - glyph.height / 2,
            )
        else:
            insert_norm = None

        return super().insert_glyph(glyph, insert=insert_norm)

    @abstractmethod
    def draw(self):
        ...

    @property
    def _glyph(self) -> BaseGlyph:
        return self

    @property
    def _container(self) -> svgwrite.container.SVG:
        return self._svg


class EmptyParams(BaseParams):
    pass


class EmptyGlyph(BaseGlyph[EmptyParams]):
    """
    Glyph to use as an on-the-fly alternative to subclassing
    {obj}`BaseGlyph`. It has an empty {obj}`BaseGlyph.draw`
    implementation; the user can then add graphics objects
    and other glyphs after creation.

    Example:

    ```python
    glyph1 = MyGlyph1()
    glyph2 = MyGlyph2()

    # create an empty glyph with unspecified size
    glyph = EmptyGlyph()

    # insert a glyph
    glyph.insert_glyph(glyph1)

    # insert another glyph in a different position
    glyph.insert_glyph(glyph2, (100, 100))
    ```
    """

    def draw(self):
        pass
