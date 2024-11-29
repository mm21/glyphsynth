"""
Provides a simple layer on top of pydantic's `BaseModel` which
supports aggregation of values.
"""
from __future__ import annotations

from typing import Any, Iterable, Self

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
        values: dict[str, Any] = {}

        for model in [m for m in models if m is not None]:
            values.update(
                model._get_values(field_filter=cls.model_fields.keys())
            )

        return cls(**values)

    def _get_values(
        self, field_filter: Iterable[str] | None = None
    ) -> dict[str, str]:
        values: dict[str, str] = {}

        for field in self.model_fields.keys():
            # handle filter if provided
            if field_filter is not None and field not in field_filter:
                continue

            # set value if non-None or explicitly set
            value = getattr(self, field)
            if value is not None or field in self.model_fields_set:
                values[field] = value

        return values
