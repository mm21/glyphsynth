from pathlib import Path
from typing_extensions import Annotated

import typer

from .export import invoke_export


app = typer.Typer(
    add_completion=False, invoke_without_command=False, no_args_is_help=True
)


# Dummy callback required in order to allow having a single subcommand
@app.callback()
def main():
    pass


@app.command(no_args_is_help=True)
def export(
    path_cls: Annotated[
        str,
        typer.Argument(help="Path to Python class, e.g. my_pkg.my_mod.MyGlyph"),
    ],
    path_output: Annotated[
        str,
        typer.Argument(
            help="Path to output file or folder; if folder, filename generated by class name"
        ),
    ],
    format: Annotated[
        str,
        typer.Argument(
            help='"svg" or "png", or leave empty to determine from filename if possible, defaulting to "svg"'
        ),
    ] = None,
):
    assert format in {"svg", "png", None}, f"Invalid format: {format}"
    invoke_export(path_cls, Path(path_output), format)


if __name__ == "__main__":
    app()
