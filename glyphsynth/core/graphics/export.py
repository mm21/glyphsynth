from __future__ import annotations

from functools import wraps
from xml.etree import ElementTree
from shutil import which
from typing import Literal
import copy
import logging
import subprocess
import os
import sys
import xml.dom.minidom as minidom

from svgwrite.drawing import Drawing
from svgwrite.container import SVG, Group

from .container import BaseContainer

__all__ = ["RASTER_SUPPORT"]

RASTER_SUPPORT: bool = os.name == "posix"


def _save_prep(ext_default: str):
    def func_wrapper(func):
        """
        Common preparation for saving to file.
        """

        @wraps(func)
        def wrapper(self: BaseContainer, path: str, *args, **kwargs):
            return self._

            # path_file: str
            is_dir: bool

            if os.path.exists(path):
                # existing path, determine if directory
                is_dir = os.path.isdir(path)
            else:
                # not existing path, use heuristics to determine if path is
                # a directory: if it doesn't have an extension, it should be
                # a directory

                dirname: str

                _, ext = os.path.splitext(path)

                is_dir = len(ext) == 0

                if is_dir:
                    # path should be a destination folder
                    dirname = path
                else:
                    # path should be a destination file
                    dirname = os.path.dirname(path)

                # create dirs if needed
                os.makedirs(dirname, exist_ok=True)

            path_file: str

            if is_dir:
                basename: str = f"{self._id}.{ext_default}"
                path_file = os.path.join(path, basename)
            else:
                path_file = path

            return func(self, path_file, *args, **kwargs)

        return wrapper

    return func_wrapper


class ExportContainer(BaseContainer):
    def export(self, path: str, format: Literal["svg", "png"] | None = None):
        # normalize format
        format_: str = self._get_format(path, format)

        print(f"--- export(): path={path}, format={format}, format_={format_}")

        match format_:
            case "svg":
                self.export_svg(path)
            case "png":
                # TODO: pass through png-specific params?
                self.export_png(path)
            case _:
                raise Exception

    def export_svg(self, path: str):
        """
        :param path: Path to destination file or folder
        """

        path_: str

        path_, _ = self._normalize_path(path, "svg")

        with open(path_, "w") as fh:
            fh.write(self._get_svg())

    def export_png(
        self,
        path: str,
        size: tuple[str, str] | None = None,
        dpi: tuple[int, int] = (96, 96),
        scale: float | int = 1,
    ):
        """
        :param path: Path to destination file or folder
        :param size: Size of image with concrete units (px/in/...), e.g. `("1in", "1in")`{l=python}, or `None`{l=python} to use provided scale factor
        :param dpi: Pixels per inch
        :param scale: Factor by which to scale user units to concrete pixels, only if `size is None`{l=python}
        """

        # normalize path
        path_: str

        path_, _ = self._normalize_path(path, "png")

        # normalize size
        size_raster: tuple[str, str] = size or self._get_size_raster(
            float(scale)
        )

        self._rasterize(path_, size_raster, dpi)

    def get_svg(self) -> str:
        return self._get_svg()

    def _get_svg(self, drawing: Drawing | None = None) -> str:
        """
        Get a string containing the full XML content.
        """

        # if no drawing provided, default to drawing for this glyph
        drawing_: Drawing = drawing or self._drawing

        # get element as string
        xml_str: str = ElementTree.tostring(
            drawing_.get_xml(), encoding="utf-8", xml_declaration=True
        ).decode("utf-8")

        xml_tree = minidom.parseString(xml_str)
        return xml_tree.toprettyxml(indent="  ")

    def _rasterize(
        self, path_png: str, size_raster: tuple[str, str], dpi: tuple[int, int]
    ):
        # ensure rsvg-convert is supported and available
        if not RASTER_SUPPORT:
            sys.exit(
                "Conversion to .png only supported on Linux due to availability of rsvg-convert"
            )

        if (path_rsvg_convert := which("rsvg-convert")) is None:
            sys.exit("Could not find path to rsvg-convert")

        logging.debug(f"Found path to rsvg-convert: {path_rsvg_convert}")

        # create temp svg file scaled appropriately
        path_svg = f"{path_png}.temp.svg"
        self._create_svg_temp(path_svg, size_raster)

        logging.info(
            f"Rasterizing: {path_svg} -> {path_png}, size_raster={size_raster}, dpi={dpi}"
        )

        # TODO: pass background color in API?
        args = [
            path_rsvg_convert,
            "--keep-aspect-ratio",
            "--background-color",
            "#ffffff",
            "--dpi-x",
            f"{dpi[0]}",
            "--dpi-y",
            f"{dpi[1]}",
            "-o",
            path_png,
            path_svg,
        ]

        logging.debug(f"Running: {' '.join(args)}")

        subprocess.check_call(args)

    def _create_svg_temp(self, path_svg: str, size_raster: tuple[str, str]):
        """
        Create temp .svg for rasterizing.
        """

        # create temp drawing (top-level <svg>) and set size in order to
        # set output size
        # - required even if size provided to rsvg-convert
        drawing_tmp: Drawing = copy.copy(self._drawing)

        self._rescale_svg(drawing_tmp, size_raster, set_size=True)

        svg_str = self._get_svg(drawing_tmp)

        with open(path_svg, "w") as fh:
            fh.write(svg_str)

    def _get_size_raster(self, scale: float):
        assert (
            self.size is not None
        ), f"No size provided for rasterizing and glyph {self} has no size"

        x = int(self.size[0] * scale)
        y = int(self.size[1] * scale)

        return (f"{x}px", f"{y}px")

    def _normalize_path(
        self, path: str, format: Literal["svg", "png"] | None
    ) -> tuple[str, str]:
        """
        Take path (folder or file) and return a tuple of (complete filename, format).
        """

        is_dir: bool

        if os.path.exists(path):
            # existing path, determine if directory
            is_dir = os.path.isdir(path)
        else:
            # not existing path, use heuristics to determine if path is
            # a directory: if it doesn't have an extension, it should be
            # a directory

            dirname: str

            _, ext = os.path.splitext(path)

            is_dir = len(ext) == 0

            if is_dir:
                # path should be a destination folder
                dirname = path
            else:
                # path should be a destination file
                dirname = os.path.dirname(path)

            # create dirs if needed
            os.makedirs(dirname, exist_ok=True)

        path_file: str
        format_: str

        format_ = self._get_format(path, format)

        if is_dir:
            basename: str = f"{self._id}.{format_}"
            path_file = os.path.join(path, basename)
        else:
            path_file = path

        return (path_file, format_)

    def _get_format(self, path: str, format: str | None) -> str:
        # check provided format
        if format is not None:
            return format

        # check path
        basename: str = os.path.basename(path)
        _, ext = os.path.splitext(basename)

        if ext != "":
            # omit "."
            return ext[1:]

        return "svg"
