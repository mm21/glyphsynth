import logging

import rich.traceback
import typer
from rich.console import Console
from rich.logging import RichHandler

from ..drawing.export import export_drawings

LEVEL = logging.INFO


app = typer.Typer(
    rich_markup_mode="rich",
    no_args_is_help=True,
    add_completion=False,
)

rich.traceback.install(show_locals=True)
logging.basicConfig(
    level=LEVEL,
    format="%(message)s",
    handlers=[
        RichHandler(
            rich_tracebacks=True,
            console=Console(),
            show_level=True,
            show_time=False,
            show_path=False,
            markup=True,
        )
    ],
)


# TODO: take size, dpi
# TODO: take params_file: str | None
# - if provided, use as params for BaseDrawing subclass imported by fqcn
# - contains mappings of drawing_id to params dict
@app.command(no_args_is_help=True)
def export(
    fqcn: str = typer.Argument(help="FQCN of drawing(s) to export"),
    output_path: str = typer.Argument(help="Output path (file or folder)"),
    output_modpath: bool = typer.Option(
        False,
        help="Whether to create subfolders based on the respective drawing's modpath",
    ),
    svg: bool = typer.Option(False, help="Write .svg to folder", is_flag=True),
    png: bool = typer.Option(
        False, help="Write .png to folder (Linux only)", is_flag=True
    ),
):
    export_drawings(
        fqcn, output_path, output_modpath=output_modpath, svg=svg, png=png
    )


def run():
    app()


if __name__ == "__main__":
    run()
