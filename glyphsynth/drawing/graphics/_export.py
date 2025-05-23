from __future__ import annotations

import copy
import logging
import re
import shutil
import subprocess
import sys
import tempfile
import xml.dom.minidom as minidom
from pathlib import Path
from typing import Literal, cast
from xml.etree import ElementTree

from svgwrite.drawing import Drawing

from . import RASTER_SUPPORT
from ._container import BaseGraphicsContainer


class ExportContainer(BaseGraphicsContainer):
    def export(
        self, path: Path, out_format: Literal["svg", "png"] | None = None
    ):
        match self._get_format(path, out_format):
            case "svg":
                self.export_svg(path)
            case "png":
                self.export_png(path)
            case _:
                raise ValueError(f"Invalid format: {out_format}")

    def export_svg(
        self,
        path: Path,
        size: tuple[str, str] | None = None,
        background: str | None = None,
    ):
        """
        :param path: Path to destination file or folder
        """

        path_norm: Path = self._normalize_path(path, "svg")
        drawing = (
            self._rescale_drawing(size) if size else copy.copy(self._drawing)
        )

        if background:
            drawing.elements.insert(
                0, drawing.rect(fill=background, size=("100%", "100%"))
            )

        with path_norm.open("w") as fh:
            fh.write(self._get_svg(drawing))

    def export_png(
        self,
        path: Path,
        size: tuple[str, str] | None = None,
        background: str | None = "#ffffff",
        dpi: tuple[int, int] = (96, 96),
        scale: float | int = 1,
        in_place_raster: bool = False,
    ):
        """
        :param path: Path to destination file or folder
        :param size: Size of image with concrete units (px/in/...), e.g. `("1in", "1in")`{l=python}, or `None`{l=python} to use provided scale factor
        :param dpi: Pixels per inch
        :param scale: Factor by which to scale user units to concrete pixels, only if `size is None`{l=python}
        """

        path_norm: Path = self._normalize_path(path, "png")
        size_raster: tuple[str, str] | None = size or self._get_size_raster(
            float(scale)
        )

        self._rasterize(
            path_norm, size_raster, background, dpi, in_place_raster
        )

    def _get_svg(self, drawing: Drawing | None = None) -> str:
        """
        Get a string containing the full XML content.
        """

        # if no drawing provided, default to drawing for this drawing
        drawing_: Drawing = drawing or self._drawing

        # get xml tree
        xml = self._fixup_xml(drawing_.get_xml())

        # get as string
        xml_bytes = cast(
            bytes, ElementTree.tostring(xml, "utf-8", xml_declaration=True)
        )
        xml_str: str = xml_bytes.decode("utf-8")

        # return formatted string
        return minidom.parseString(xml_str).toprettyxml(indent="  ")

    def _fixup_xml(self, xml: ElementTree.Element):
        """
        Traverse element tree and replace ids to ensure determinism
        (same drawing xml is generated each time). Since svgwrite's id factory
        is global, the ids can be changed by unrelated drawing creation.
        """

        pattern = r"(id\d+)"

        # mapping of old ids to new ones
        id_map: dict[str, str] = {}

        # convert old to new id
        def convert_id(id_: str) -> str:
            if id_ not in id_map:
                id_map[id_] = (
                    f"id{len(id_map) + 1}"
                    if re.match(f"^{pattern}$", id_)
                    else id_
                )
            return id_map[id_]

        # convert a value like "url(#id7)" to the remapped id, otherwise
        # pass through existing value
        def convert_val(val: str) -> str:
            def replace_match(match: re.Match):
                return f"#{convert_id(match.group(1))}"

            return re.sub(f"#{pattern}", replace_match, val)

        # process <defs>
        def process_defs(defs: ElementTree.Element):
            for e in defs:
                id_ = e.get("id")
                assert id_ is not None
                e.set("id", convert_id(id_))

        def process_elem(elem: ElementTree.Element):
            # handle any <defs>
            if (defs := elem.find("defs")) is not None:
                process_defs(defs)

            # handle any replacements in this element
            for attr, val in elem.attrib.items():
                elem.set(attr, convert_val(val))

            # recurse into children
            for e in elem:
                process_elem(e)

        process_elem(xml)
        return xml

    def _rasterize(
        self,
        path_png: Path,
        size_raster: tuple[str, str] | None,
        background: str | None,
        dpi: tuple[int, int],
        in_place_raster: bool,
    ):
        # ensure rsvg-convert is supported and available
        if not RASTER_SUPPORT:
            sys.exit(
                "Conversion to .png only supported on Linux due to availability of rsvg-convert"
            )

        if (path_rsvg_convert := shutil.which("rsvg-convert")) is None:
            sys.exit("Could not find path to rsvg-convert")

        logging.debug(f"Found path to rsvg-convert: {path_rsvg_convert}")

        # create temp svg file scaled appropriately
        path_svg: Path

        path_svg_dir = (
            path_png.parent if in_place_raster else Path(tempfile.mkdtemp())
        )

        path_svg = path_svg_dir / f"{path_png.name}.temp.svg"
        self._create_svg_temp(path_svg, size_raster)

        if size_raster is None:
            logging.warning(
                f"Rasterizing a drawing which has no outermost size, output image size may be unexpected: {self}"
            )

        logging.debug(
            f"Rasterizing: {path_svg} -> {path_png}, size_raster={size_raster}, dpi={dpi}"
        )

        background_args = (
            ["--background-color", background] if background else []
        )

        args = (
            [path_rsvg_convert, "--keep-aspect-ratio"]
            + background_args
            + [
                "--dpi-x",
                f"{dpi[0]}",
                "--dpi-y",
                f"{dpi[1]}",
                "-o",
                str(path_png),
                str(path_svg),
            ]
        )

        logging.debug(f"Running: {' '.join(args)}")

        subprocess.check_call(args)

        # clean up temp dir
        if not in_place_raster:
            shutil.rmtree(path_svg.parent)

    def _rescale_drawing(self, size: tuple[str, str]) -> Drawing:
        """
        Rescale this drawing.
        """
        drawing: Drawing = copy.copy(self._drawing)
        self._rescale_svg(drawing, size, self._size_norm, set_size=True)
        return drawing

    def _create_svg_temp(
        self, path_svg: Path, size_raster: tuple[str, str] | None
    ):
        """
        Create temp .svg for rasterizing.
        """

        # create temp drawing (top-level <svg>) and set size in order to
        # set output size
        # - required even if size provided to rsvg-convert
        drawing_tmp = self._rescale_drawing(size_raster)

        with path_svg.open("w") as fh:
            fh.write(self._get_svg(drawing_tmp))

    def _get_size_raster(self, scale: float) -> tuple[str, str] | None:
        if not self.has_size:
            return None

        x = int(self.size[0] * scale)
        y = int(self.size[1] * scale)

        return (f"{x}px", f"{y}px")

    def _normalize_path(
        self, path: Path, out_format: Literal["svg", "png"] | None
    ) -> Path:
        """
        Take path (folder or file) and return complete filename.
        """

        out_format_norm = self._get_format(path, out_format)
        is_dir: bool

        if path.exists():
            # existing path, determine if directory
            is_dir = path.is_dir()
        else:
            # not existing path, use heuristics to determine if path is
            # a directory: if it doesn't have an extension, it should be
            # a directory

            is_dir = len(path.suffix) == 0
            path_dir = path if is_dir else path.parent

            # create dirs if needed
            path_dir.mkdir(parents=True, exist_ok=True)

        return path / f"{self._id_norm}.{out_format_norm}" if is_dir else path

    def _get_format(self, path: Path, format: str | None) -> str:
        # check provided format
        if format is not None:
            return format

        # check path
        if len(path.suffix):
            # omit "."
            return path.suffix[1:]

        # default to svg
        return "svg"
