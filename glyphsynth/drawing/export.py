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

from .drawing import BaseDrawing

__all__ = [
    "ExportSpec",
    "export_drawings",
]

type DrawingObjType = type[BaseDrawing] | BaseDrawing | ExportSpec
"""
Represents a drawing to be exported. If a BaseDrawing subclass or instance is
provided, an ExportSpec is automatically created using the output path.
"""

type DrawingSpecType = DrawingObjType | Iterable[DrawingSpecType] | Callable[
    [], DrawingSpecType
]
"""
Recursive type to represent an object which can be handled by exporter.
"""

INDENT = 4


@dataclass
class ExportSpec:
    """
    Container for a drawing instance and path in which to place the exported
    artifact.
    """

    drawing: BaseDrawing
    path: Path
    module: str | None = None


def export_drawings(
    fqcn: str,
    output_path: Path,
    output_modpath: bool = False,
    svg: bool = False,
    png: bool = False,
    in_place_raster: bool = False,
):
    """
    Export all drawings from the object imported from the fully-qualified
    class name, which may be any of the following:

    - ExportSpec
    - BaseDrawing subclass or instance
    - Iterable
    - Callable
    - Module with symbol names provided via `__all__`

    The object imported from the FQCN is recursed to collect all drawing objects.
    If a `BaseDrawing` is encountered,
    """

    logging.info(f"Exporting to output path: {output_path}")

    containers: list[ExportSpec] = _extract_containers(fqcn)

    for container in containers:
        export_path: Path

        if output_modpath:
            # if enabled, include drawing's modpath in output path hierarchy
            module = container.module or container.drawing.__module__
            export_path = (
                output_path / module.replace(".", "/") / container.path
            )
        else:
            export_path = output_path / container.path

        _export_drawing(
            container.drawing,
            export_path,
            svg,
            png,
            in_place_raster,
        )


def _export_drawing(
    drawing: BaseDrawing,
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
        logging.info(f"Writing svg: {drawing} -> {path}.svg")
        drawing.export_svg(export_path)

    if png:
        logging.info(f"Writing png: {drawing} -> {path}.png")
        drawing.export_png(export_path, in_place_raster=in_place_raster)


def _extract_containers(fqcn: str) -> list[ExportSpec]:
    """
    Extract all drawings from the provided FQCN, which may be any of the
    following:

    - BaseDrawing subclass or instance
    - Iterable of the above (subclasses and instances can be intermixed)
    - Callable which returns any of the above
    - Module containing any of the above, with symbol names provided via
      `__all__`
    """

    drawing_specs: list[DrawingSpecType]

    drawing_specs = _import_drawing_specs(fqcn)
    containers: list[ExportSpec] = _normalize_drawing_specs(drawing_specs)

    return containers


def _import_drawing_specs(fqcn: str) -> list[DrawingSpecType]:
    drawing_specs: list[DrawingSpecType]

    module: ModuleType | None = None
    obj: DrawingSpecType | None = None
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

    drawing_specs: list[Any] = _import_all(module) if obj is None else [obj]
    return cast(list[DrawingSpecType], drawing_specs)


def _normalize_drawing_specs(
    drawing_specs: list[DrawingSpecType],
) -> list[ExportSpec]:
    """
    Take an object and return a list of ExportSpec instances.
    """

    containers: list[ExportSpec] = []

    for drawing_spec in drawing_specs:
        containers_extract = _recurse_drawing_spec(drawing_spec)

        # validate returned objects
        for container in containers_extract:
            assert isinstance(container, ExportSpec)
            containers.append(container)

    return containers


def _recurse_drawing_spec(
    drawing_spec: DrawingSpecType,
) -> list[DrawingSpecType]:
    """
    Recurse into drawing spec until we find a drawing class, drawing instance, or
    export spec. A container will be created if not found.
    """

    ret: list[ExportSpec] = []

    if isinstance(drawing_spec, ExportSpec):
        ret.append(drawing_spec)

    elif isinstance(drawing_spec, BaseDrawing):
        ret.append(ExportSpec(drawing_spec, Path()))

    elif isinstance(drawing_spec, Iterable):
        for spec in drawing_spec:
            ret += _recurse_drawing_spec(spec)

    # function, BaseDrawing subclass, or BaseVariantFactory subclass
    elif isinstance(drawing_spec, Callable):
        ret += _recurse_drawing_spec(drawing_spec())

    else:
        raise Exception(f"Invalid drawing_spec: {drawing_spec}")

    return ret


def _import_all(module: ModuleType) -> list[Any]:
    all_: list[str] | None = None
    objs: list[Any] = []

    try:
        all_ = module.__all__
    except AttributeError:
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
