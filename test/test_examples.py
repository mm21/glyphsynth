from glyphsynth import BaseParams, BaseGlyph

ZERO: float = 0.0
UNIT: float = 1000.0
HALF: float = UNIT / 2

UNIT_SIZE: tuple[float, float] = (UNIT, UNIT)
ORIGIN: tuple[float, float] = (ZERO, ZERO)


FRACTAL_DEPTH = 10


class UnitGlyph[ParamsT: BaseParams](BaseGlyph[ParamsT]):
    size_canon = UNIT_SIZE


class SquareParams(BaseParams):
    color_upper_left: str
    color_upper_right: str
    color_lower_left: str
    color_lower_right: str


class SquareGlyph(UnitGlyph[SquareParams]):
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
    square_params: SquareParams
    depth: int = FRACTAL_DEPTH


class SquareFractalGlyph(UnitGlyph[SquareFractalParams]):
    def draw(self):
        # draw square
        self.insert_glyph(SquareGlyph(params=self.params.square_params))

        # draw another fractal glyph
        if self.params.depth > 1:
            child_params = SquareFractalParams(
                square_params=self.params.square_params,
                depth=self.params.depth - 1,
            )
            child_glyph = SquareFractalGlyph(
                params=child_params, size=(HALF, HALF)
            )

            child_glyph.rotate(90.0)

            self.insert_glyph(child_glyph, insert=(HALF / 2, HALF / 2))


def test_square(output_dir: str):
    square_params = SquareParams(
        color_upper_left="red",
        color_upper_right="orange",
        color_lower_right="green",
        color_lower_left="blue",
    )

    square = SquareGlyph(params=square_params)
    square.export_svg(output_dir)


def test_fractal(output_dir: str):
    square_params = SquareParams(
        color_upper_left="rgb(250, 50, 0)",
        color_upper_right="rgb(250, 250, 0)",
        color_lower_right="rgb(0, 250, 50)",
        color_lower_left="rgb(0, 50, 250)",
    )

    fractal = SquareFractalGlyph(
        params=SquareFractalParams(square_params=square_params)
    )
    fractal.export_svg(output_dir)
    fractal.export_png(output_dir, size=("4096px", "4096px"))
