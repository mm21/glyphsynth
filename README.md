# GlyphSynth

[![Python versions](https://img.shields.io/pypi/pyversions/glyphsynth.svg)](https://pypi.org/project/glyphsynth)
[![PyPI](https://img.shields.io/pypi/v/glyphsynth?color=%2334D058&label=pypi%20package)](https://pypi.org/project/glyphsynth)
[![Tests](./badges/tests.svg?dummy=8484744)]()
[![Coverage](./badges/cov.svg?dummy=8484744)]()
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

- [GlyphSynth](#glyphsynth)
  - [Motivation](#motivation)
  - [Getting started](#getting-started)
  - [Interface](#interface)
  - [Exporting](#exporting)
    - [Programmatically](#programmatically)
    - [CLI](#cli)
  - [Examples](#examples)
    - [Multi-square](#multi-square)
    - [Multi-square fractal](#multi-square-fractal)
    - [Gradients](#gradients)
    - [Letter combination variants](#letter-combination-variants)


## Motivation

This project provides a Pythonic mechanism to construct SVG graphics, termed as "glyphs". Glyphs can be parameterized and leverage inheritance to promote reuse. The ability to construct many variations of glyphs programmatically is a powerful tool for creativity.

## Getting started

First, install using pip:

```bash
pip install glyphsynth
```

The user is intended to develop glyphs using their own Python modules. A typical workflow might be to create a number of `BaseGlyph` subclasses, set them in `__all__`, and invoke `glyphsynth-export` passing in the module and output path. See below for more details.

## Interface

Glyphs can be constructed in two ways, or a combination of both:

- Subclass `BaseGlyph` and implement `draw()`
    - Parameterize with a subclass of `BaseParams` corresponding to the glyph
- Create an instance of `EmptyGlyph` (or any other `BaseGlyph` subclass) and invoke draw APIs

In its `draw()` method, a `BaseGlyph` subclass can invoke drawing APIs which create corresponding SVG objects. SVG properties are automatically propagated to SVG objects from the glyph's properties, `BaseGlyph.properties`, which can be provided at runtime with defaults being specified by the subclass.

A simple example of implementing `draw()` to draw a blue square:

```python
from glyphsynth import BaseParams, BaseGlyph, ShapeProperties

# Glyph params
class MySquareParams(BaseParams):
    color: str

# Glyph subclass
class MySquareGlyph(BaseGlyph[MySquareParams]):

    # Canonical size for glyph construction, can be rescaled upon creation
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


# Create glyph instance
blue_square = MySquareGlyph(
    glyph_id="blue-square", params=MySquareParams(color="blue")
)

# Render as image
blue_square.export_png(Path("my_glyph_renders"))
```

This is rendered as:

[![Blue-square](./examples/blue-square.png)]()

Equivalently, the same glyph can be constructed from an `EmptyGlyph`:

```python
from glyphsynth import EmptyGlyph

blue_square = EmptyGlyph(glyph_id="blue-square", size=(100, 100))

# Draw a centered square
blue_square.draw_rect(
    (25.0, 25.0), (50.0, 50.0), properties=ShapeProperties(fill="blue")
)

# Draw a black border around the perimeter
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

### Programmatically

A glyph is exported as an `.svg` file. Rasterizing to `.png` is supported on Linux and requires the following packages:

```bash
sudo apt install librsvg2-bin libmagickwand-dev
```

A glyph can be exported using `BaseGlyph.export()`, `BaseGlyph.export_svg()`, or `BaseGlyph.export_png()`. If a folder is passed as the output path, the glyph's `glyph_id` will be used to derive the filename.

```python
from pathlib import Path

# Export to specific path
blue_square.export(Path("my_glyph_renders/blue-square.svg"))
blue_square.export(Path("my_glyph_renders/blue-square.png"))

# Export using class name as filename
blue_square.export_svg(Path("my_glyph_renders")) # blue-square.svg 
blue_square.export_png(Path("my_glyph_renders")) # blue-square.png
```

### CLI

The CLI tool `glyphsynth-export` exports glyphs by importing a Python object. See `glyphsynth-export --help` for full details.

The object can be any of the following:

- Module, from which objects will be extracted via `__all__`
- `BaseGlyph` subclass
- `BaseGlyph` instance
- Iterable
- Callable

Any `BaseGlyph` subclasses found will be instantiated using their respective default parameters. For `Iterable` and `Callable`, the object is traversed or invoked recursively until glyph subclasses or instances are found.

Assuming the above code containing the `blue_square` is placed in `my_glyphs.py`, the glyph can be exported to `my_glyph_renders/` via the following command:

`glyphsynth-export my_glyphs.blue_square my_glyph_renders --svg --png`

## Examples

### Multi-square

[![Multi-square](./examples/multi-square.png)]()

This glyph is composed of 4 nested squares, each with a color parameter.

```python
from glyphsynth import BaseParams, BaseGlyph

# Definitions
ZERO: float = 0.0
UNIT: float = 100.0
HALF: float = UNIT / 2
UNIT_SIZE: tuple[float, float] = (UNIT, UNIT)
ORIGIN: tuple[float, float] = (ZERO, ZERO)

# Multi-square parameters
class MultiSquareParams(BaseParams):
    color_upper_left: str
    color_upper_right: str
    color_lower_left: str
    color_lower_right: str

# Multi-square glyph class
class MultiSquareGlyph(BaseGlyph[MultiSquareParams]):

    size_canon = UNIT_SIZE

    def draw(self):

        # Each nested square should occupy 1/4 of the area
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

# Create parameters
multi_square_params = MultiSquareParams(
    color_upper_left="red",
    color_upper_right="orange",
    color_lower_right="green",
    color_lower_left="blue",
)

# Create glyph
multi_square = MultiSquareGlyph(glyph_id="multi-square", params=multi_square_params)
```

### Multi-square fractal

[![Multi-square fractal](./examples/multi-square-fractal.png)]()

This glyph nests a square glyph recursively up to a certain depth.

```python
from glyphsynth import BaseParams, BaseGlyph

# Maximum recursion depth for creating fractal
FRACTAL_DEPTH = 10

class SquareFractalParams(BaseParams):
    square_params: MultiSquareParams
    depth: int = FRACTAL_DEPTH

class SquareFractalGlyph(BaseGlyph[SquareFractalParams]):

    size_canon = UNIT_SIZE

    def draw(self):

        # Draw square
        self.insert_glyph(MultiSquareGlyph(params=self.params.square_params))

        if self.params.depth > 1:
            # Draw another fractal glyph, half the size and rotated 90 degrees

            child_params = SquareFractalParams(
                square_params=self.params.square_params,
                depth=self.params.depth - 1,
            )
            child_glyph = SquareFractalGlyph(
                params=child_params, size=(HALF, HALF)
            )

            # Rotate and insert in center
            child_glyph.rotate(90.0)
            self.insert_glyph(child_glyph, insert=(HALF / 2, HALF / 2))

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
```

### Gradients

[![Sunset gradient](./examples/sunset-gradients.png)]()

This illustrates the use of gradients and glyph composition to create a simple ocean sunset scene.

```python
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
        sky_reflection = SkyGlyph(properties=Properties(opacity="0.5"))
        ocean = OceanGlyph()

        # rotate reflection
        sky_reflection.rotate(180)

        self.insert_glyph(sky)
        self.insert_glyph(ocean, insert=(0, self.height / 2))
        self.insert_glyph(sky_reflection, insert=(0, self.height / 2))

scene = SceneGlyph()
```

### Letter combination variants

[![Variants matrix](./examples/variants-matrix-pad.png)]()

This illustrates the use of letter glyphs, provided by this package as a library, to create parameterized geometric designs. Permutations of pairs of letters `A`, `M`, and `T` are selected for a range of color variants, with the second letter being rotated 180 degrees.

```python
from glyphsynth.lib.alphabet.minimal import (
    UNIT,
    LetterParams,
    BaseLetterGlyph,
    LetterComboParams,
    BaseLetterComboGlyph,
    A,
    M,
    T,
)

# Letters to use for variants
LETTERS = [
    A,
    M,
    T,
]

# Colors to use for variants
COLORS = [
    "black",
    "red",
    "green",
    "blue",
]

# Params containing 2 letters which are overlayed
class AMTComboParams(LetterComboParams):
    letter1: type[BaseLetterGlyph]
    letter2: type[BaseLetterGlyph]

# Glyph class
class AMTComboGlyph(BaseLetterComboGlyph[AMTComboParams]):
    def draw(self):
        
        # draw letters given by params
        self.draw_letter(self.params.letter1)
        letter2 = self.draw_letter(self.params.letter2)

        # additionally rotate letter2
        letter2.rotate(180)
```

A subclass of `BaseVariantExportFactory` can be used as a convenience for generating variants:

```python
from typing import Generator
import itertools

from glyphsynth.lib.variants import BaseVariantExportFactory

# Factory to create variants of AMTComboGlyph
class VariantFactory(BaseVariantExportFactory[AMTComboGlyph]):

    # Width of resulting matrix
    MATRIX_WIDTH = len(COLORS)

    # Top-level padding and space between glyph variants
    SPACING = UNIT / 10

    # Glyph subclass from which to generate variants
    glyph_cls = AMTComboGlyph

    # Generate variants of colors and letter combinations
    def get_params_variants(self) -> Generator[AMTComboParams, None, None]:
        for color, letter1, letter2 in itertools.product(
            COLORS, LETTERS, LETTERS
        ):
            yield AMTComboParams(
                letter_params=LetterParams(color=color),
                letter1=letter1,
                letter2=letter2,
            )
```

The fully-qualified class name of `VariantFactory` can be passed as an argument to `glyphsynth-export`. This will result in a folder structure containing each variant individually, as well as the variant matrix and each individual row/column.
