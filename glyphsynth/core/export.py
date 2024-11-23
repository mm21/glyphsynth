"""
Export functionality, wrapped by CLI and can be used programmatically.
"""

import importlib
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Iterable, cast

from glyphsynth import BaseGlyph

__all__ = [
    "RASTER_SUPPORT",
    "ExportSpec",
    "export_glyphs",
]

type GlyphObjType = type[BaseGlyph] | BaseGlyph | ExportSpec
"""
Represents a glyph to be exported. If a BaseGlyph subclass or instance is
provided, an ExportSpec is automatically created using the output path.
"""

type GlyphSpecType = GlyphObjType | Iterable[GlyphSpecType] | Callable[
    [], GlyphSpecType
]
"""
Recursive type to represent an object which can be handled by exporter.
"""

INDENT = 4


@dataclass
class ExportSpec:
    """
    Container for a glyph instance and path in which to place the exported
    artifact.
    """

    glyph: BaseGlyph
    path: Path
    module: str | None = None


def export_glyphs(
    fqcn: str,
    output_path: Path,
    output_modpath: bool = False,
    svg: bool = False,
    png: bool = False,
    in_place_raster: bool = False,
):
    """
    Export all glyphs from the object imported from the fully-qualified
    class name, which may be any of the following:

    - ExportSpec
    - BaseGlyph subclass or instance
    - Iterable
    - Callable
    - Module with symbol names provided via `__all__`

    The object imported from the FQCN is recursed to collect all glyph objects.
    If a `BaseGlyph` is encountered,

    """

    logging.info(f"Exporting to output path: {output_path}")

    containers: list[ExportSpec] = _extract_containers(fqcn)

    for container in containers:
        export_path: Path

        if output_modpath:
            # if enabled, include glyph's modpath in output path hierarchy
            module = container.module or container.glyph.__module__
            export_path = (
                output_path / module.replace(".", "/") / container.path
            )
        else:
            export_path = output_path / container.path

        _export_glyph(
            container.glyph,
            export_path,
            svg,
            png,
            in_place_raster,
        )


def _export_glyph(
    glyph: BaseGlyph,
    export_path: Path,
    svg: bool,
    png: bool,
    in_place_raster: bool,
):
    cwd = Path(os.getcwd())
    path = (
        export_path.relative_to(cwd)
        if export_path.is_relative_to(cwd)
        else export_path
    )

    if svg:
        logging.info(f"Writing svg: {glyph.glyph_id} -> {path}.svg")
        glyph.export_svg(export_path)

    if png:
        logging.info(f"Writing png: {glyph.glyph_id} -> {path}.png")
        glyph.export_png(export_path, in_place_raster=in_place_raster)


def _extract_containers(fqcn: str) -> list[ExportSpec]:
    """
    Extract all glyphs from the provided FQCN, which may be any of the
    following:

    - BaseGlyph subclass or instance
    - Iterable of the above (subclasses and instances can be intermixed)
    - Callable which returns any of the above
    - Module containing any of the above, with symbol names provided via
      `__all__`
    """

    glyph_specs: list[GlyphSpecType]

    glyph_specs = _import_glyph_specs(fqcn)
    containers: list[ExportSpec] = _normalize_glyph_specs(glyph_specs)

    return containers


def _import_glyph_specs(fqcn: str) -> list[GlyphSpecType]:
    glyph_specs: list[GlyphSpecType]

    module: ModuleType | None = None
    obj: GlyphSpecType | None = None
    import_excep: ImportError | AttributeError | None = None

    try:
        # attempt to import module
        module = importlib.import_module(fqcn)
    except ImportError as e:
        import_excep = e

    if module is None and "." in fqcn:
        # attempt to import object from module
        module_path, obj_name = fqcn.rsplit(".", 1)

        try:
            module = importlib.import_module(module_path)
            obj = getattr(module, obj_name)
        except (ImportError, AttributeError) as e:
            import_excep = e
        else:
            # clear exception as we successfully imported the object
            import_excep = None

    if import_excep is not None:
        logging.error(f"Failed to import object: {fqcn}")
        raise import_excep

    assert module is not None

    glyph_specs: list[Any] = _import_all(module) if obj is None else [obj]
    return cast(list[GlyphSpecType], glyph_specs)


def _normalize_glyph_specs(
    glyph_specs: list[GlyphSpecType],
) -> list[ExportSpec]:
    """
    Take an object and return a list of ExportSpec instances.
    """

    containers: list[ExportSpec] = []

    for glyph_spec in glyph_specs:
        containers_extract = _recurse_glyph_spec(glyph_spec)

        # validate returned objects
        for container in containers_extract:
            assert isinstance(container, ExportSpec)
            containers.append(container)

    return containers


def _recurse_glyph_spec(glyph_spec: GlyphSpecType) -> list[GlyphSpecType]:
    """
    Recurse into glyph spec until we find a glyph class, glyph instance, or
    export spec. A container will be created if not found.
    """

    ret: list[ExportSpec] = []

    if isinstance(glyph_spec, ExportSpec):
        ret.append(glyph_spec)

    elif isinstance(glyph_spec, BaseGlyph):
        ret.append(ExportSpec(glyph_spec, Path()))

    elif isinstance(glyph_spec, Iterable):
        for spec in glyph_spec:
            ret += _recurse_glyph_spec(spec)

    # function, BaseGlyph subclass, or BaseVariantExportFactory subclass
    elif isinstance(glyph_spec, Callable):
        ret += _recurse_glyph_spec(glyph_spec())

    else:
        raise Exception(f"Invalid glyph_spec: {glyph_spec}")

    return ret


def _import_all(module: ModuleType) -> list[Any]:
    all_: list[str] | None = None
    objs: list[Any] = []

    try:
        all_ = module.__all__
    except Exception:
        pass

    assert all_ is not None, f"Module does not have attribute __all__: {module}"

    for attr in all_:
        obj: Any | None = None
        try:
            obj = getattr(module, attr)
        except AttributeError:
            pass

        assert obj is not None, f"Failed to import {attr} from {module}"
        objs.append(obj)

    return objs
