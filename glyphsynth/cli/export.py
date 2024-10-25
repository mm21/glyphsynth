from pathlib import Path
from types import ModuleType
from typing import Any, Literal
import logging

from ..core.glyph import BaseGlyph


def invoke_export(
    path_cls: str, path_output: Path, format: Literal["svg", "png"] | None
):
    logging.info(
        f"Exporting: modpath={path_cls}, path_output={path_output}, format={format}"
    )

    # get class to be imported
    glyph_cls: type[BaseGlyph] = _get_glyph_cls(path_cls)

    # instantiate glyph
    glyph: BaseGlyph = glyph_cls()

    # export glyph
    glyph.export(path_output, format)


def _get_glyph_cls(path_cls: str) -> type[BaseGlyph]:
    modpath: str
    cls_name: str

    modpath, cls_name = _parse_path_cls(path_cls)

    mod: ModuleType = __import__(modpath, fromlist=[cls_name])
    glyph_cls: Any = getattr(mod, cls_name)

    assert issubclass(glyph_cls, BaseGlyph)
    return glyph_cls


def _parse_path_cls(path_cls: str) -> tuple[str, str]:
    """
    Return modpath and class name.
    """
    modpath: str
    cls_name: str

    path_split: list[str] = path_cls.rsplit(".", maxsplit=1)
    assert len(path_split) == 2, f"Invalid path_cls: {path_cls}"

    modpath, cls_name = path_split

    return (modpath, cls_name)
