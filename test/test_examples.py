from pathlib import Path

from glyphsynth import BaseParams, BaseGlyph


from .conftest import write_glyph


ZERO: float = 0.0
UNIT: float = 1000.0
HALF: float = UNIT / 2

UNIT_SIZE: tuple[float, float] = (UNIT, UNIT)
ORIGIN: tuple[float, float] = (ZERO, ZERO)


FRACTAL_DEPTH = 10


class MySquareParams(BaseParams):
    color: str


class MySquareGlyph(BaseGlyph[MySquareParams]):
    size_canon = (100.0, 100.0)

    def draw(self):
        # Draw a rectangle using the provided color
        self.draw_rect((25.0, 25.0), (50.0, 50.0), fill=self.params.color)

        # Draw a black border around the perimeter
        self.draw_polyline(
            [(0.0, 0.0), (0.0, 100.0), (100.0, 100.0), (100.0, 0), (0.0, 0.0)],
            stroke="black",
            fill="none",
            stroke_width="5",
        )


class UnitGlyph[ParamsT: BaseParams](BaseGlyph[ParamsT]):
    size_canon = UNIT_SIZE


class MultiSquareParams(BaseParams):
    color_upper_left: str
    color_upper_right: str
    color_lower_left: str
    color_lower_right: str


class MultiSquareGlyph(UnitGlyph[MultiSquareParams]):
    def draw(self):
        size: tuple[float, float] = (HALF, HALF)

        # upper left
        self.draw_rect(ORIGIN, size, fill=self.params.color_upper_left)

        # upper right
        self.draw_rect((HALF, ZERO), size, fill=self.params.color_upper_right)

        # lower left
        self.draw_rect((ZERO, HALF), size, fill=self.params.color_lower_left)

        # lower right
        self.draw_rect((HALF, HALF), size, fill=self.params.color_lower_right)


class SquareFractalParams(BaseParams):
    square_params: MultiSquareParams
    depth: int = FRACTAL_DEPTH


class SquareFractalGlyph(UnitGlyph[SquareFractalParams]):
    def draw(self):
        # draw square
        self.insert_glyph(MultiSquareGlyph(params=self.params.square_params))

        if self.params.depth > 1:
            # draw another fractal glyph, half the size and rotated 90 degrees

            child_params = SquareFractalParams(
                square_params=self.params.square_params,
                depth=self.params.depth - 1,
            )
            child_glyph = SquareFractalGlyph(
                params=child_params, size=(HALF, HALF)
            )

            child_glyph.rotate(90.0)
            self.insert_glyph(child_glyph, insert=(HALF / 2, HALF / 2))


def test_blue_square(output_dir: Path):
    blue_square = MySquareGlyph(
        glyph_id="blue-square", params=MySquareParams(color="blue")
    )
    write_glyph(output_dir, blue_square)


def test_square(output_dir: Path):
    multi_square_params = MultiSquareParams(
        color_upper_left="red",
        color_upper_right="orange",
        color_lower_right="green",
        color_lower_left="blue",
    )

    multi_square = MultiSquareGlyph(
        glyph_id="multi-square", params=multi_square_params
    )
    write_glyph(output_dir, multi_square)


def test_fractal(output_dir: Path):
    multi_square_params = MultiSquareParams(
        color_upper_left="rgb(250, 50, 0)",
        color_upper_right="rgb(250, 250, 0)",
        color_lower_right="rgb(0, 250, 50)",
        color_lower_left="rgb(0, 50, 250)",
    )

    fractal = SquareFractalGlyph(
        glyph_id="multi-square-fractal",
        params=SquareFractalParams(square_params=multi_square_params),
    )

    fractal.export_svg(output_dir)
    fractal.export_png(
        output_dir, size=("4096px", "4096px"), in_place_raster=True
    )
