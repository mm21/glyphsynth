from pathlib import Path

from glyphsynth import (
    BaseGlyph,
    BaseParams,
    EmptyGlyph,
    Properties,
    ShapeProperties,
)

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

    blue_square2 = EmptyGlyph(glyph_id="blue-square-2", size=(100, 100))

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

    write_glyph(output_dir, blue_square2)


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


def test_gradients(output_dir: Path):
    WIDTH = 400
    HEIGHT = 300

    class SkyGlyph(BaseGlyph):
        size_canon = (WIDTH, HEIGHT / 2)

        def draw(self):
            sky = self.draw_rect((0, 0), (WIDTH, HEIGHT / 2))
            sky.fill(
                gradient=self.create_radial_gradient(
                    center=(self.width / 2, self.height),
                    radius=self.width / 2,
                    focal=(self.width / 2, self.height * 1.5),
                    colors=["yellow", "orange", "#00a6e6"],
                )
            )

    class OceanGlyph(BaseGlyph):
        size_canon = (WIDTH, HEIGHT / 2)

        def draw(self):
            water = self.draw_rect((0, 0), (WIDTH, HEIGHT / 2))
            water.fill(
                gradient=self.create_linear_gradient(
                    start=(self.width / 2, 0),
                    end=(self.width / 2, self.height),
                    colors=["#7295b6", "#0f4c81"],
                )
            )

    class SceneGlyph(BaseGlyph):
        size_canon = (WIDTH, HEIGHT)

        def draw(self):
            sky = SkyGlyph()
            sky_reflection = SkyGlyph(properties=Properties(opacity=0.5))
            ocean = OceanGlyph()

            # rotate reflection
            sky_reflection.rotate(180)

            self.insert_glyph(sky)
            self.insert_glyph(ocean, insert=(0, self.height / 2))
            self.insert_glyph(sky_reflection, insert=(0, self.height / 2))

    scene = SceneGlyph()

    write_glyph(output_dir, scene, scale=3)
