from types import ModuleType
from typing import Any, Literal

from ..core.glyph import BaseGlyph


def invoke_export(
    path_cls: str, path_output: str, format: Literal["svg", "png"] | None
):
    print(
        f"Exporting: modpath={path_cls}, path_output={path_output}, format={format}"
    )

    # get class to be imported
    glyph_cls: type[BaseGlyph] = _get_glyph_cls(path_cls)

    print(f"--- got glyph_cls: {glyph_cls}")

    # instantiate glyph
    glyph: BaseGlyph = glyph_cls()

    # export glyph
    glyph.export(path_output, format)


def _get_glyph_cls(path_cls: str) -> type[BaseGlyph]:
    modpath: str
    cls_name: str

    modpath, cls_name = _parse_path_cls(path_cls)

    print(f"--- importing {cls_name} from {modpath}")

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
