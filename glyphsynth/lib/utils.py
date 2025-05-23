from typing import Literal

from ..drawing import BaseDrawing, BaseParams

__all__ = [
    "PaddingType",
    "PaddingParams",
    "PaddingDrawing",
    "extend_line",
]

type SideType = Literal["top", "bottom", "left", "right"]

type PaddingType = dict[SideType, float]

SIDES: list[SideType] = ["top", "bottom", "left", "right"]


class PaddingParams(BaseParams):
    drawing: BaseDrawing
    padding: float | PaddingType = 0.0


class PaddingDrawing(BaseDrawing[PaddingParams]):
    _padding: PaddingType

    @classmethod
    def new(
        cls,
        drawing: BaseDrawing,
        drawing_id: str | None = None,
        padding: float | PaddingType | None = None,
    ):
        padding_: float | PaddingType

        # default padding is 10% of the minimum of width/height
        padding_ = (
            min(drawing.width, drawing.height) / 10
            if padding is None
            else padding
        )

        # create params
        params = cls.get_params_cls()(drawing=drawing, padding=padding_)

        # get drawing id
        glyph_id_ = drawing_id or (
            f"{drawing.drawing_id}-pad" if drawing.drawing_id else None
        )

        return cls(drawing_id=glyph_id_, params=params)

    def init(self):
        self._padding = self._get_padding()
        self.canonical_size = self._get_size()

    def draw(self):
        self.insert_drawing(
            self.params.drawing, (self._padding["left"], self._padding["top"])
        )

    def _get_padding(self) -> PaddingType:
        padding: PaddingType

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
            self.params.drawing.size[0]
            + self._padding["left"]
            + self._padding["right"]
        )
        height = float(
            self.params.drawing.size[1]
            + self._padding["top"]
            + self._padding["bottom"]
        )

        return (width, height)


# TODO: caption drawing
# - optional custom caption; default based on class name and params


def extend_line(
    start: tuple[float, float], end: tuple[float, float], scale: float = 1.0
) -> tuple[float, float]:
    """
    Convenience function to return a point along a line collinear with
    the provided start and end.

    The distance between `point` and the returned point is the distance between
    `point` and `ref` scaled by the provided `scale`.
    """

    offset: tuple[float, float] = (end[0] - start[0], end[1] - start[1])
    offset_scale: tuple[float, float] = (offset[0] * scale, offset[1] * scale)

    return (
        end[0] + offset_scale[0],
        end[1] + offset_scale[1],
    )
