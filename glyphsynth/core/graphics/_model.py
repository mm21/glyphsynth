"""
Provides a simple layer on top of pydantic's `BaseModel` which
supports aggregation of values.
"""
from __future__ import annotations

from typing import Any, Self, cast

from pydantic import BaseModel

__all__ = [
    "BaseFieldsModel",
]


class BaseFieldsModel(BaseModel):
    @classmethod
    def _aggregate(cls, *models: BaseFieldsModel | None) -> Self:
        """
        Create a new model with values aggregated from provided models.
        """
        values: dict[str, str] = {}
        fields: list[str] = cls._get_fields()

        for model in [m for m in models if m is not None]:
            for key, value in model._get_values().items():
                if key in fields:
                    values[key] = value

        return cls(**values)

    @classmethod
    def _get_fields(cls) -> list[str]:
        return list(cls.model_fields.keys())

    def _get_values(self) -> dict[str, str]:
        values: dict[str, str] = {}

        for field in type(self)._get_fields():
            value = cast(Any | None, getattr(self, field))
            if value is not None:
                values[field] = value

        return values
