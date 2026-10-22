from pathlib import Path

from doit.task import Task
from pyprojkit import TaskFactory

globals().update(TaskFactory().create_all_tasks())

TEST_OUT_PATH = Path("test/__out__")

ASSETS_PATH = Path("assets")
LOGO_HEIGHT = 300

EXAMPLES_PATH = ASSETS_PATH / "examples"
EXAMPLES: list[str | tuple[str, str]] = [
    "test_blue_square/blue-square.png",
    "test_runic_alphabet/runic-alphabet.png",
    ("test_glyphsynth_logo/glyphsynth-logo-pad.svg", "glyphsynth-logo.svg"),
    (
        "test_letter_combination_variants/variants/matrix/matrix.png",
        "letter-combination-variants.png",
    ),
    "test_sunset_gradients/sunset-gradients.png",
    "test_multi_square/multi-square.png",
    "test_multi_square/multi-square-fractal.png",
]
"""
List of examples to copy from test output to examples folder.
"""


def task_logo() -> Task:
    logo_light_path = ASSETS_PATH / "logo-light.svg"
    logo_dark_path = ASSETS_PATH / "logo-dark.svg"

    def run():
        from glyphsynth import GlyphParams
        from glyphsynth.lib.logo import GlyphSynthLogo

        dark_params = GlyphParams(color="white")

        logo_light = GlyphSynthLogo()
        logo_dark = GlyphSynthLogo(params=dark_params)

        width = LOGO_HEIGHT * (logo_light.width / logo_light.height)
        height = LOGO_HEIGHT
        size = (f"{width}px", f"{height}px")

        logo_light.export_svg(logo_light_path, size=size)
        logo_dark.export_svg(logo_dark_path, size=size)

    return Task(
        "logo",
        actions=[run],
        targets=[logo_light_path, logo_dark_path],
        file_dep=["src/glyphsynth/lib/logo.py"],
        clean=True,
    )


def task_examples() -> Task:
    # normalize to list of (src path, dest filename) tuples
    examples_norm: list[tuple[str, str]] = [
        example if isinstance(example, tuple) else (example, Path(example).name)
        for example in EXAMPLES
    ]

    # collect source/target paths
    sources = [
        str(TEST_OUT_PATH / "test_examples" / src_path) for src_path, _ in examples_norm
    ]
    targets = [str(EXAMPLES_PATH / dest_filename) for _, dest_filename in examples_norm]

    return Task(
        "examples",
        actions=[f"cp {source} {target}" for source, target in zip(sources, targets)],
        targets=targets,
        file_dep=sources,
        clean=[f"rm -rf {EXAMPLES_PATH}/*"],
    )
