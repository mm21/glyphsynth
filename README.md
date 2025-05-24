<p align="center">
  <img src="./assets/logo.svg" alt="Logo" />
</p>

# GlyphSynth
Pythonic vector graphics synthesis toolkit

[![Python versions](https://img.shields.io/pypi/pyversions/glyphsynth.svg)](https://pypi.org/project/glyphsynth)
[![PyPI](https://img.shields.io/pypi/v/glyphsynth?color=%2334D058&label=pypi%20package)](https://pypi.org/project/glyphsynth)
[![Tests](./badges/tests.svg?dummy=8484744)]()
[![Coverage](./badges/cov.svg?dummy=8484744)]()
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

- [GlyphSynth](#glyphsynth)
  - [Motivation](#motivation)
  - [Getting started](#getting-started)
  - [Drawing interface](#drawing-interface)
  - [Exporting](#exporting)
    - [Programmatically](#programmatically)
    - [CLI](#cli)
  - [Examples](#examples)
    - [Glyphs](#glyphs)
      - [Runic alphabet](#runic-alphabet)
      - [GlyphSynth logo](#glyphsynth-logo)
      - [Letter combination variants](#letter-combination-variants)
    - [Drawings](#drawings)
      - [Sunset gradients](#sunset-gradients)
      - [Multi-square](#multi-square)
      - [Multi-square fractal](#multi-square-fractal)


## Motivation

This project provides a Pythonic mechanism to construct SVG drawings. Drawings can be parameterized and leverage composition and inheritance to promote reuse. The ability to construct many variations of drawings programmatically can be a powerful tool for creativity.

This project's goal is to specialize in the creation of glyphs &mdash; symbols conveying some meaning. The unique Pythonic approach can be ideal for anything from logos to artwork.

Nonetheless it evolved to become a more general-purpose vector graphics framework, essentially providing a layer of abstraction on top of `svgwrite`. The underlying graphics synthesis capability is planned to be split off into a separate project, with GlyphSynth continuing to offer a more specialized interface for glyphs specifically.

## Getting started

First, install using pip:

```bash
pip install glyphsynth
```

The user is intended to develop graphics using their own Python modules. A typical workflow might be to create a number of `BaseDrawing` subclasses, set them in `__all__`, and invoke `glyphsynth-export` passing in the module and output path. See below for more details.

## Drawing interface

The drawing interface largely borrows the structure and terminology of `svgwrite`, with some enhancements along with type safety. The top-level graphics element is therefore the "drawing". Drawings can be constructed in two ways, or a combination of both:

- Subclass `BaseDrawing` and implement `draw()`
    - Parameterize with a subclass of `BaseParams` corresponding to the `BaseDrawing` subclass
- Create an instance of `Drawing` (or any other `BaseDrawing` subclass) and invoke draw APIs

In its `draw()` method, a `BaseDrawing` subclass can invoke drawing APIs which create corresponding SVG objects. SVG properties are automatically propagated to SVG objects from the drawing's properties, `BaseDrawing.properties`, which can be provided upon creation with defaults specified by the subclass.

A simple example of implementing `draw()` to draw a blue square:

<p align="center">
  <img src="./assets/examples/blue-square.png" alt="Blue square" />
</p>

```python
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

# render as image
blue_square.export_png(Path("my-drawings"))
```

Equivalently, the same drawing can be constructed from a `Drawing`:

```python
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
```

## Exporting

A drawing is primarily exported as an `.svg` file. Rasterizing to `.png` is supported on Linux and requires the following packages:

```bash
sudo apt install librsvg2-bin libmagickwand-dev
```

### Programmatically

A drawing can be exported using `BaseDrawing.export()`, `BaseDrawing.export_svg()`, or `BaseDrawing.export_png()`. If a folder is passed as the output path, the drawing's `drawing_id` will be used to derive the filename.

```python
from pathlib import Path

my_drawings = Path("my-drawings")

# export to specific file, format auto-detected
blue_square.export(my_drawings / "blue-square.svg")
blue_square.export(my_drawings / "blue-square.png")

# export to folder using drawing_id as filename
blue_square.export_svg(my_drawings) # blue-square.svg
blue_square.export_png(my_drawings) # blue-square.png
```

### CLI

The CLI tool `glyphsynth-export` exports drawings by importing a Python object. See `glyphsynth-export --help` for full details.

The object can be any of the following:

- Module, from which objects will be extracted via `__all__`
- `BaseDrawing` subclass
- `BaseDrawing` instance
- Iterable
- Callable

Any `BaseDrawing` subclasses found will be instantiated using their respective default parameters. For `Iterable` and `Callable`, the object is traversed or invoked recursively until drawing subclasses or instances are found.

Assuming the above code containing the `blue_square` is placed in `my_drawings.py`, the drawing can be exported to `my-drawings/` via the following command:

`glyphsynth-export my_drawings.blue_square my-drawings --svg --png`

## Examples

### Glyphs

#### Runic alphabet

As part of `glyphsynth.lib`, an alphabet of rune-style glyphs is provided. These are designed to be overlayed and form geometric shapes.

<p align="center">
  <img src="./assets/examples/runic-alphabet.svg" alt="Runic letter matrix" />
</p>

```python
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
```

#### GlyphSynth logo

This project's logo is formed by combining the runic glyphs `G` and `S`:

<p align="center">
  <img src="./assets/examples/glyphsynth-logo.svg" alt="Project logo" />
</p>

```python
from glyphsynth import Glyph

class GlyphSynthLogo(Glyph):
    def draw(self):
        self.draw_glyph(G)
        self.draw_glyph(S, scale=0.5)

glyphsynth_logo = GlyphSynthLogo(drawing_id="glyphsynth-logo")
```

Note the `S` glyph is scaled by one half, remaining centered in the parent glyph. While its size is reduced, its stroke width is increased accordingly to match the parent glyph.

#### Letter combination variants

This illustrates the use of runic letter glyphs to create parameterized geometric designs. Combinations of pairs of letters `A`, `M`, and `Y` are selected for a range of stroke widths, with the second letter being rotated 180 degrees.

<p align="center">
  <img src="./assets/examples/letter-combination-variants.png" alt="Letter variant matrix" width="300" />
</p>

```python
from glyphsynth.glyph import UNIT, BaseGlyph, GlyphParams
from glyphsynth.lib.alphabets.latin.runic import A, M, Y

# letters to combine
LETTERS = [A, M, Y]

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
```

A subclass of `BaseVariantFactory` can be used as a convenience for generating variants:

```python
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
```

The fully-qualified class name of `LetterVariantFactory` can be passed as an argument to `glyphsynth-export`. This will result in a folder structure containing each variant individually, as well as the variant matrix and each individual row/column.

### Drawings

The following examples illustrate the use of the generic drawing capability developed for this project.

#### Sunset gradients

This illustrates the use of gradients and drawing composition to create a simple ocean sunset scene.

<p align="center">
  <img src="./assets/examples/sunset-gradients.png" alt="Sunset gradients" />
</p>

```python
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
```

#### Multi-square

This drawing is composed of 4 nested squares, each with a color parameter.

<p align="center">
  <img src="./assets/examples/multi-square.png" alt="Multi-square" width="300" />
</p>

```python
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
```

#### Multi-square fractal

This drawing nests a multi-square drawing recursively up to a certain depth.

<p align="center">
  <img src="./assets/examples/multi-square-fractal.png" alt="Multi-square fractal" width="300" />
</p>

```python
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
```
