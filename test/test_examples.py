from pathlib import Path

from .conftest import write_drawing


def test_blue_square(output_dir: Path):
    from glyphsynth import BaseDrawing, BaseParams, ShapeProperties

    # drawing params
    class MySquareParams(BaseParams):
        color: str

    # drawing subclass
    class MySquareDrawing(BaseDrawing[MySquareParams]):
        # canonical size for drawing construction, can be rescaled upon creation
        canonical_size = (100.0, 100.0)

        def draw(self):
            # draw a centered square using the provided color
            self.draw_rect(
                (25.0, 25.0),
                (50.0, 50.0),
                properties=ShapeProperties(fill=self.params.color),
            )

            # draw a black border around the perimeter
            self.draw_polyline(
                [
                    (0.0, 0.0),
                    (0.0, 100.0),
                    (100.0, 100.0),
                    (100.0, 0),
                    (0.0, 0.0),
                ],
                properties=ShapeProperties(
                    stroke="black",
                    fill="none",
                    stroke_width="5",
                ),
            )

    # create drawing instance
    blue_square = MySquareDrawing(
        drawing_id="blue-square", params=MySquareParams(color="blue")
    )

    write_drawing(output_dir, blue_square)

    from glyphsynth import Drawing

    blue_square = Drawing(drawing_id="blue-square", size=(100, 100))

    # draw a centered square
    blue_square.draw_rect(
        (25.0, 25.0), (50.0, 50.0), properties=ShapeProperties(fill="blue")
    )

    # draw a black border around the perimeter
    blue_square.draw_polyline(
        [(0.0, 0.0), (0.0, 100.0), (100.0, 100.0), (100.0, 0), (0.0, 0.0)],
        properties=ShapeProperties(
            stroke="black",
            fill="none",
            stroke_width="5",
        ),
    )

    write_drawing(output_dir / "blue-square-2", blue_square)


def test_runic_alphabet(output_dir: Path):
    from glyphsynth import MatrixDrawing
    from glyphsynth.lib.alphabets.latin.runic import (
        LETTER_CLASSES,
        BaseRunicGlyph,
    )

    # instantiate letters and split into 2 rows
    rows: list[list[BaseRunicGlyph]] = [
        [letter_cls() for letter_cls in LETTER_CLASSES[:13]],
        [letter_cls() for letter_cls in LETTER_CLASSES[13:]],
    ]

    # create matrix of letters
    matrix = MatrixDrawing.new(rows, drawing_id="runic-alphabet", spacing=10)

    write_drawing(output_dir, matrix, background="#ffffff")


def test_glyphsynth_logo(output_dir: Path):
    from glyphsynth.lib.logo import GlyphSynthLogo

    glyphsynth_logo = GlyphSynthLogo(drawing_id="glyphsynth-logo")

    write_drawing(output_dir, glyphsynth_logo, background="#ffffff")


def test_letter_combination_variants(output_dir: Path):
    from glyphsynth.glyph import UNIT, BaseGlyph, GlyphParams
    from glyphsynth.lib.alphabets.latin.runic import A, M, Y

    # letters to combine
    LETTERS = [
        A,
        M,
        Y,
    ]

    # stroke widths (in percents) to iterate over
    STROKE_PCTS = [2.5, 5, 7.5]

    class LetterComboParams(GlyphParams):
        letter1: type[BaseGlyph]
        letter2: type[BaseGlyph]

    class LetterComboGlyph(BaseGlyph[LetterComboParams]):
        def draw(self):
            # draw letters given by params, rotating letter2
            self.draw_glyph(self.params.letter1)
            self.draw_glyph(self.params.letter2).rotate(180)

    import itertools
    from typing import Generator

    from glyphsynth.lib.variants import BaseVariantFactory

    # factory to produce variants of LetterComboGlyph with different params
    class LetterVariantFactory(BaseVariantFactory[LetterComboGlyph]):
        MATRIX_WIDTH = len(STROKE_PCTS)
        SPACING = UNIT / 10

        # generate variants of stroke widths and letter combinations
        def get_params_variants(
            self,
        ) -> Generator[LetterComboParams, None, None]:
            for letter1, letter2, stroke_pct in itertools.product(
                LETTERS, LETTERS, STROKE_PCTS
            ):
                yield LetterComboParams(
                    stroke_pct=stroke_pct,
                    letter1=letter1,
                    letter2=letter2,
                )

    for spec in LetterVariantFactory():
        write_drawing(output_dir / spec.path, spec.drawing, scale=2)


def test_sunset_gradients(output_dir: Path):
    from glyphsynth import BaseDrawing, BaseParams, StopColor

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

    class SunParams(BaseParams):
        colors: list[StopColor]
        focal_scale: float

    class SunDrawing(BaseDrawing[SunParams]):
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
        sun_params: SunParams

    class SunsetDrawing(BaseDrawing[SceneParams]):
        canonical_size = (WIDTH, HEIGHT)

        def draw(self):
            # background
            self.insert_drawing(
                BackgroundDrawing(params=self.params.background_params),
                insert=(0, 0),
            )

            # sunset
            self.insert_drawing(
                SunDrawing(params=self.params.sun_params),
                insert=(0, 0),
            )

            # sunset reflection
            self.insert_drawing(
                SunDrawing(params=self.params.sun_params)
                .rotate(180)
                .fill(opacity_pct=50.0),
                insert=(0, self.center_y),
            )

    sunset = SunsetDrawing(
        drawing_id="sunset-gradients",
        params=SceneParams(
            background_params=BackgroundParams(
                sky_colors=["#1a2b4c", "#9b4e6c"],
                water_colors=["#2d3d5e", "#0f1c38"],
            ),
            sun_params=SunParams(
                colors=[
                    StopColor("#ffd700", 0.0, 100.0),
                    StopColor("#ff7f50", 50.0, 90.0),
                    StopColor("#ff6b6b", 100.0, 25.0),
                ],
                focal_scale=1.2,
            ),
        ),
    )

    write_drawing(output_dir, sunset, scale=2)

    for nested in sunset._nested_glyphs:
        write_drawing(output_dir, nested)


def test_multi_square(output_dir: Path):
    from glyphsynth import BaseDrawing, BaseParams, ShapeProperties

    # definitions
    ZERO = 0.0
    UNIT = 1000
    HALF = UNIT / 2
    UNIT_SIZE: tuple[float, float] = (UNIT, UNIT)
    ORIGIN: tuple[float, float] = (ZERO, ZERO)

    # multi-square parameters
    class MultiSquareParams(BaseParams):
        color_upper_left: str
        color_upper_right: str
        color_lower_left: str
        color_lower_right: str

    # multi-square drawing class
    class MultiSquareDrawing(BaseDrawing[MultiSquareParams]):
        canonical_size = UNIT_SIZE

        def draw(self):
            # each nested square should occupy 1/4 of the area
            size: tuple[float, float] = (HALF, HALF)

            # draw upper left
            self.draw_rect(
                ORIGIN,
                size,
                properties=ShapeProperties(fill=self.params.color_upper_left),
            )

            # draw upper right
            self.draw_rect(
                (HALF, ZERO),
                size,
                properties=ShapeProperties(fill=self.params.color_upper_right),
            )

            # draw lower left
            self.draw_rect(
                (ZERO, HALF),
                size,
                properties=ShapeProperties(fill=self.params.color_lower_left),
            )

            # draw lower right
            self.draw_rect(
                (HALF, HALF),
                size,
                properties=ShapeProperties(fill=self.params.color_lower_right),
            )

    # create parameters
    multi_square_params = MultiSquareParams(
        color_upper_left="rgb(250, 50, 0)",
        color_upper_right="rgb(250, 250, 0)",
        color_lower_right="rgb(0, 250, 50)",
        color_lower_left="rgb(0, 50, 250)",
    )

    # create drawing
    multi_square = MultiSquareDrawing(
        drawing_id="multi-square", params=multi_square_params
    )

    write_drawing(output_dir, multi_square)

    # maximum recursion depth for creating fractal
    FRACTAL_DEPTH = 10

    class SquareFractalParams(BaseParams):
        square_params: MultiSquareParams
        depth: int = FRACTAL_DEPTH

    class SquareFractalDrawing(BaseDrawing[SquareFractalParams]):
        canonical_size = UNIT_SIZE

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
                child_drawing = SquareFractalDrawing(
                    params=child_params, size=(HALF, HALF)
                )

                # rotate and insert in center
                child_drawing.rotate(90.0)
                self.insert_drawing(child_drawing, insert=(HALF / 2, HALF / 2))

    multi_square_fractal = SquareFractalDrawing(
        drawing_id="multi-square-fractal",
        params=SquareFractalParams(square_params=multi_square_params),
    )

    write_drawing(output_dir, multi_square_fractal)
