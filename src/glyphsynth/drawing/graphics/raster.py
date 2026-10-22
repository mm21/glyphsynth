import os

__all__ = [
    "RASTER_SUPPORT",
]

RASTER_SUPPORT: bool = os.name == "posix"
"""
Whether rasterization is supported; Linux only.
"""
