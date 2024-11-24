from __future__ import annotations

from typing import Any, TypeVar, get_args


def extract_type_param[
    T, U
](cls: type[T], param_cls: type[U]) -> type[U] | None:
    """
    Extract the type param with the given class.
    """

    orig_bases = cls.__orig_bases__  # pyright: ignore[reportGeneralTypeIssues]
    assert len(orig_bases)

    args = get_args(orig_bases[0])
    if len(args):
        param: type[U]

        if isinstance(args[0], TypeVar):
            # have a TypeVar, look up its bound
            type_var = args[0]
            assert type_var.__bound__ is not None
            param = type_var.__bound__
        else:
            # already have a class
            param = args[0]

        assert issubclass(param, param_cls)
        return param

    return None


def normalize_str(v: Any | None) -> str | None:
    return None if v is None else str(v)
