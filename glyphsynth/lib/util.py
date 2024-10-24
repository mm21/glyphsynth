from typing import Literal

from ..core import BaseGlyph, BaseParams


__all__ = [
    "PaddingSpec",
    "PaddingParams",
    "PaddingGlyph",
]

type SideSpec = Literal["top", "bottom", "left", "right"]

type PaddingSpec = dict[SideSpec, float]

# TODO: get from SideSpec to avoid redundancy
SIDES: list[SideSpec] = ["top", "bottom", "left", "right"]


class PaddingParams(BaseParams):
    glyph: BaseGlyph
    padding: float | PaddingSpec


class PaddingGlyph(BaseGlyph[PaddingParams]):
    _padding: PaddingSpec

    @classmethod
    def new(cls, glyph: BaseGlyph, padding: float | PaddingSpec | None = None):
        padding_: float | PaddingSpec

        # default padding is 10% of the minimum of width/height
        padding_ = (
            min(glyph.width, glyph.height) / 10 if padding is None else padding
        )

        # create params
        params = cls.params_cls(glyph=glyph, padding=padding_)

        # generate glyph id
        glyph_id_ = f"{glyph.glyph_id}-pad"

        return cls(glyph_id=glyph_id_, params=params)

    def init(self):
        self._padding = self._get_padding()
        self.size_canon = self._get_size()

    def draw(self):
        self.insert_glyph(
            self.params.glyph, (self._padding["left"], self._padding["top"])
        )

    def _get_padding(self) -> PaddingSpec:
        padding: PaddingSpec

        if isinstance(self.params.padding, dict):
            padding = self.params.padding.copy()
        else:
            padding = {side: float(self.params.padding) for side in SIDES}

        for side in padding:
            assert side in SIDES, f"Invalid side: {side}"

        for side in SIDES:
            if side not in padding:
                padding[side] = 0.0

        return padding

    def _get_size(self) -> tuple[float, float]:
        width = float(
            self.params.glyph.size[0]
            + self._padding["left"]
            + self._padding["right"]
        )
        height = float(
            self.params.glyph.size[1]
            + self._padding["top"]
            + self._padding["bottom"]
        )

        return (width, height)


# TODO: caption glyph
# - optional custom caption; default based on class name and params
