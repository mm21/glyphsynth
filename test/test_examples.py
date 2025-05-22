import itertools
from pathlib import Path
from typing import Generator

from glyphsynth import (
    BaseDrawing,
    BaseParams,
    Drawing,
    ShapeProperties,
    StopColor,
)

from .conftest import write_drawing

ZERO: float = 0.0
UNIT: float = 1000.0
HALF: float = UNIT / 2

UNIT_SIZE: tuple[float, float] = (UNIT, UNIT)
ORIGIN: tuple[float, float] = (ZERO, ZERO)


FRACTAL_DEPTH = 10


class MySquareParams(BaseParams):
    color: str


class MySquareDrawing(BaseDrawing[MySquareParams]):
    canonical_size = (100.0, 100.0)

    def draw(self):
        # Draw a centered square using the provided color
        self.draw_rect(
            (25.0, 25.0),
            (50.0, 50.0),
            properties=ShapeProperties(fill=self.params.color),
        )

        # Draw a black border around the perimeter
        self.draw_polyline(
            [(0.0, 0.0), (0.0, 100.0), (100.0, 100.0), (100.0, 0), (0.0, 0.0)],
            properties=ShapeProperties(
                stroke="black",
                fill="none",
                stroke_width="5",
            ),
        )


class UnitDrawing[ParamsT: BaseParams](BaseDrawing[ParamsT]):
    canonical_size = UNIT_SIZE


class MultiSquareParams(BaseParams):
    color_upper_left: str
    color_upper_right: str
    color_lower_left: str
    color_lower_right: str


class MultiSquareDrawing(UnitDrawing[MultiSquareParams]):
    def draw(self):
        size: tuple[float, float] = (HALF, HALF)

        # Draw upper left
        self.draw_rect(
            ORIGIN,
            size,
            properties=ShapeProperties(fill=self.params.color_upper_left),
        )

        # Draw upper right
        self.draw_rect(
            (HALF, ZERO),
            size,
            properties=ShapeProperties(fill=self.params.color_upper_right),
        )

        # Draw lower left
        self.draw_rect(
            (ZERO, HALF),
            size,
            properties=ShapeProperties(fill=self.params.color_lower_left),
        )

        # Draw lower right
        self.draw_rect(
            (HALF, HALF),
            size,
            properties=ShapeProperties(fill=self.params.color_lower_right),
        )


class SquareFractalParams(BaseParams):
    square_params: MultiSquareParams
    depth: int = FRACTAL_DEPTH


class SquareFractalDrawing(UnitDrawing[SquareFractalParams]):
    def draw(self):
        # draw square
        self.insert_drawing(
            MultiSquareDrawing(params=self.params.square_params)
        )

        if self.params.depth > 1:
            # draw another fractal drawing, half the size and rotated 90 degrees

            child_params = SquareFractalParams(
                square_params=self.params.square_params,
                depth=self.params.depth - 1,
            )
            child_glyph = SquareFractalDrawing(
                params=child_params, size=(HALF, HALF)
            )

            child_glyph.rotate(90.0)
            self.insert_drawing(child_glyph, insert=(HALF / 2, HALF / 2))


def test_blue_square(output_dir: Path):
    blue_square = MySquareDrawing(
        drawing_id="blue-square", params=MySquareParams(color="blue")
    )

    write_drawing(output_dir, blue_square)

    blue_square2 = Drawing(drawing_id="blue-square-2", size=(100, 100))

    # Draw a centered square
    blue_square2.draw_rect(
        (25.0, 25.0), (50.0, 50.0), properties=ShapeProperties(fill="blue")
    )

    # Draw a black border around the perimeter
    blue_square2.draw_polyline(
        [(0.0, 0.0), (0.0, 100.0), (100.0, 100.0), (100.0, 0), (0.0, 0.0)],
        properties=ShapeProperties(
            stroke="black",
            fill="none",
            stroke_width="5",
        ),
    )

    write_drawing(output_dir, blue_square2)


def test_square(output_dir: Path):
    multi_square_params = MultiSquareParams(
        color_upper_left="red",
        color_upper_right="orange",
        color_lower_right="green",
        color_lower_left="blue",
    )

    multi_square = MultiSquareDrawing(
        drawing_id="multi-square", params=multi_square_params
    )
    write_drawing(output_dir, multi_square)


def test_fractal(output_dir: Path):
    multi_square_params = MultiSquareParams(
        color_upper_left="rgb(250, 50, 0)",
        color_upper_right="rgb(250, 250, 0)",
        color_lower_right="rgb(0, 250, 50)",
        color_lower_left="rgb(0, 50, 250)",
    )

    fractal = SquareFractalDrawing(
        drawing_id="multi-square-fractal",
        params=SquareFractalParams(square_params=multi_square_params),
    )

    fractal.export_svg(output_dir)
    fractal.export_png(
        output_dir, size=("4096px", "4096px"), in_place_raster=True
    )


def test_sunset_gradients(output_dir: Path):
    WIDTH = 800
    HEIGHT = 600

    class BackgroundParams(BaseParams):
        sky_colors: list[str]
        water_colors: list[str]

    class BackgroundDrawing(BaseDrawing[BackgroundParams]):
        canonical_size = (WIDTH, HEIGHT)

        def draw(self):
            sky_insert, sky_size = (0.0, 0.0), (self.width, self.center_y)
            water_insert, water_size = (0.0, self.center_y), (
                self.width,
                self.center_y,
            )

            # draw sky
            self.draw_rect(sky_insert, sky_size).fill(
                gradient=self.create_linear_gradient(
                    start=(self.center_x, 0),
                    end=(self.center_x, self.center_y),
                    colors=self.params.sky_colors,
                )
            )

            # draw water
            self.draw_rect(water_insert, water_size).fill(
                gradient=self.create_linear_gradient(
                    start=(self.center_x, self.center_y),
                    end=(self.center_x, self.height),
                    colors=self.params.water_colors,
                )
            )

    class SunsetParams(BaseParams):
        colors: list[StopColor]
        focal_scale: float

    class SunsetDrawing(BaseDrawing[SunsetParams]):
        canonical_size = (WIDTH, HEIGHT / 2)

        def draw(self):
            insert, size = (0.0, 0.0), (self.width, self.height)

            self.draw_rect(insert, size).fill(
                gradient=self.create_radial_gradient(
                    center=(self.center_x, self.height),
                    radius=self.center_x,
                    focal=(
                        self.center_x,
                        self.height * self.params.focal_scale,
                    ),
                    colors=self.params.colors,
                )
            )

    class SceneParams(BaseParams):
        background_params: BackgroundParams
        sunset_params: SunsetParams

    class SceneDrawing(BaseDrawing[SceneParams]):
        canonical_size = (WIDTH, HEIGHT)

        def draw(self):
            # background
            self.insert_drawing(
                BackgroundDrawing(params=self.params.background_params),
                insert=(0, 0),
            )

            # sunset
            self.insert_drawing(
                SunsetDrawing(params=self.params.sunset_params),
                insert=(0, 0),
            )

            # sunset reflection
            self.insert_drawing(
                SunsetDrawing(params=self.params.sunset_params)
                .rotate(180)
                .fill(opacity_pct=50.0),
                insert=(0, self.center_y),
            )

    scene = SceneDrawing(
        drawing_id="sunset",
        params=SceneParams(
            background_params=BackgroundParams(
                sky_colors=["#1a2b4c", "#9b4e6c"],
                water_colors=["#2d3d5e", "#0f1c38"],
            ),
            sunset_params=SunsetParams(
                colors=[
                    StopColor("#ffd700", 0.0, 100.0),
                    StopColor("#ff7f50", 50.0, 90.0),
                    StopColor("#ff6b6b", 100.0, 25.0),
                ],
                focal_scale=1.2,
            ),
        ),
    )

    write_drawing(output_dir, scene, scale=2)

    for nested in scene._nested_glyphs:
        write_drawing(output_dir, nested)


def test_runic_letter_matrix(output_dir: Path):
    from glyphsynth import MatrixDrawing
    from glyphsynth.lib.alphabets.latin.runic import (
        LETTER_CLASSES,
        BaseRunicGlyph,
    )

    ROWS, COLS = 2, 13

    rows: list[list[BaseRunicGlyph]] = [[] for _ in range(ROWS)]

    # place each letter in a row
    for letter_idx, letter_cls in enumerate(LETTER_CLASSES):
        row_idx = letter_idx // COLS
        rows[row_idx].append(letter_cls())

    # create matrix of letters
    matrix = MatrixDrawing.new(
        rows, drawing_id="runic-letter-matrix", spacing=10
    )

    write_drawing(output_dir, matrix)


def test_letter_variants(output_dir: Path):
    from glyphsynth.glyph import BaseGlyph, GlyphParams
    from glyphsynth.lib import MatrixDrawing
    from glyphsynth.lib.alphabets.latin.runic import A, M, T
    from glyphsynth.lib.variants import BaseVariantExportFactory

    LETTERS = [
        A,
        M,
        T,
    ]

    COLORS = [
        "black",
        "red",
        "green",
        "blue",
    ]

    class AMTComboParams(GlyphParams):
        letter1: type[BaseGlyph]
        letter2: type[BaseGlyph]

    class AMTComboGlyph(BaseGlyph[AMTComboParams]):
        def draw(self):
            # draw letters given by params
            self.draw_glyph(self.params.letter1)
            letter2 = self.draw_glyph(self.params.letter2)

            # additionally rotate letter2
            letter2.rotate(180)

    class AMTVariantFactory(BaseVariantExportFactory[AMTComboGlyph]):
        MATRIX_WIDTH = len(COLORS)
        SPACING = UNIT / 10

        # generate variants of colors and letter combinations
        def get_params_variants(self) -> Generator[AMTComboParams, None, None]:
            for letter1, letter2, color in itertools.product(
                LETTERS, LETTERS, COLORS
            ):
                yield AMTComboParams(
                    color=color,
                    letter1=letter1,
                    letter2=letter2,
                )

    rows: list[list[AMTComboGlyph]] = []

    for letter1, letter2 in itertools.product(LETTERS, LETTERS):
        row = []

        for color in COLORS:
            drawing = AMTComboGlyph(
                params=AMTComboParams(
                    color=color,
                    letter1=letter1,
                    letter2=letter2,
                )
            )
            row.append(drawing)
        rows.append(row)

    matrix = MatrixDrawing.new(
        rows,
        drawing_id="amt-combo-matrix",
        spacing=10,
    )
    write_drawing(output_dir, matrix)

    for spec in AMTVariantFactory():
        write_drawing(output_dir / spec.path, spec.drawing)


def test_logo(output_dir: Path):
    from glyphsynth.lib.logo import GlyphSynthLogo

    logo = GlyphSynthLogo(drawing_id="glyphsynth-logo")
    write_drawing(output_dir, logo)
