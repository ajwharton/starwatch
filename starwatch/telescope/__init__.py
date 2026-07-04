"""Telescope control abstractions."""

from starwatch.telescope.coordinates import EquatorialCoord, resolve_target

__all__ = [
    "EquatorialCoord",
    "resolve_target",
]