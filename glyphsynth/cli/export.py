import logging
import typer

from ..core.export import export_glyphs


app = typer.Typer(
    rich_markup_mode="rich",
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    add_completion=False,
)


# TODO: take size, dpi
@app.command(no_args_is_help=True)
def export(
    fqcn: str = typer.Argument(help="FQCN of glyph(s) to export"),
    output_path: str = typer.Argument(help="Output path (file or folder)"),
    output_modpath: bool = typer.Option(
        False,
        help="Whether to create subfolders based on the respective glyph's modpath",
    ),
    svg: bool = typer.Option(False, help="Output .svg"),
    png: bool = typer.Option(False, help="Output .png from .svg (Linux only)"),
):
    logging.info(f"Writing to output path: {output_path}")
    export_glyphs(
        fqcn, output_path, output_modpath=output_modpath, svg=svg, png=png
    )


def run():
    app()


if __name__ == "__main__":
    run()
