from pathlib import Path

from doit.task import Task
from doit.tools import create_folder

PACKAGE = "glyphsynth"

BADGES_PATH = Path("badges")
PYTEST_BADGE = BADGES_PATH / "tests.svg"
COV_BADGE = BADGES_PATH / "cov.svg"

OUT_PATH = Path("__out__")

TESTS_PATH = OUT_PATH / "tests"
JUNIT_PATH = TESTS_PATH / "junit.xml"
COV_PATH = TESTS_PATH / "cov"

COV_HTML_PATH = COV_PATH / "html"
COV_XML_PATH = COV_PATH / "coverage.xml"

LOGO_PATH = "assets/logo.svg"
LOGO_HEIGHT = 300

TEST_OUT_PATH = Path("test/__out__")

EXAMPLES_PATH = Path("assets/examples")
EXAMPLES: list[str | tuple[str, str]] = [
    "test_blue_square/blue-square.png",
    "test_runic_alphabet/runic-alphabet.svg",
    "test_glyphsynth_logo/glyphsynth-logo.svg",
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


def task_pytest():
    """
    Run pytest and generate coverage reports.
    """

    args = [
        "pytest",
        f"--cov={PACKAGE}",
        f"--cov-report=html:{COV_HTML_PATH}",
        f"--cov-report=xml:{COV_XML_PATH}",
        f"--junitxml={JUNIT_PATH}",
    ]

    return Task(
        "pytest",
        actions=[
            (create_folder, [COV_PATH]),
            # run pytest
            " ".join(args),
        ],
        targets=[
            f"{COV_HTML_PATH}/index.html",
            COV_XML_PATH,
            JUNIT_PATH,
        ],
        file_dep=[],
        clean=True,
    )


def task_badges():
    """
    Generate badges from coverage results.
    """

    gen_tests = [
        "genbadge",
        "tests",
        f"-i {JUNIT_PATH}",
        f"-o {PYTEST_BADGE}",
    ]

    gen_cov = [
        "genbadge",
        "coverage",
        f"-i {COV_XML_PATH}",
        f"-o {COV_BADGE}",
    ]

    return Task(
        "badges",
        actions=[
            (create_folder, [BADGES_PATH]),
            " ".join(gen_tests),
            " ".join(gen_cov),
        ],
        targets=[
            PYTEST_BADGE,
            COV_BADGE,
        ],
        file_dep=[
            JUNIT_PATH,
            COV_XML_PATH,
        ],
    )


def task_format() -> Task:
    """
    Run formatters.
    """

    autoflake_args = [
        "autoflake",
        "--remove-all-unused-imports",
        "--remove-unused-variables",
        "-i",
        "-r",
        ".",
    ]

    isort_args = [
        "isort",
        ".",
    ]

    black_args = [
        "black",
        ".",
    ]

    toml_sort_args = [
        "toml-sort",
        "-i",
        "pyproject.toml",
    ]

    return Task(
        "format",
        actions=[
            " ".join(autoflake_args),
            " ".join(isort_args),
            " ".join(black_args),
            " ".join(toml_sort_args),
        ],
        targets=[],
        file_dep=[],
    )


def task_logo() -> Task:
    def run():
        from glyphsynth.lib.logo import GlyphSynthLogo

        logo = GlyphSynthLogo()

        width = LOGO_HEIGHT * (logo.width / logo.height)
        height = LOGO_HEIGHT

        logo.export_svg(
            Path(LOGO_PATH),
            size=(f"{width}px", f"{height}px"),
            background="#ffffff",
        )

    return Task(
        "logo",
        actions=[run],
        targets=[LOGO_PATH],
        file_dep=["glyphsynth/lib/logo.py"],
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
        str(TEST_OUT_PATH / "test_examples" / src_path)
        for src_path, _ in examples_norm
    ]
    targets = [
        str(EXAMPLES_PATH / dest_filename) for _, dest_filename in examples_norm
    ]

    return Task(
        "examples",
        actions=[
            f"cp {source} {target}" for source, target in zip(sources, targets)
        ],
        targets=targets,
        file_dep=sources,
        clean=[f"rm -rf {EXAMPLES_PATH}/*"],
    )
