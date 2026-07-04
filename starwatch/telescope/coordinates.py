"""Coordinate parsing and conversion helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class EquatorialCoord:
    """Right ascension (hours) and declination (degrees)."""

    ra_hours: float
    dec_degrees: float

    def __post_init__(self) -> None:
        if not 0 <= self.ra_hours < 24:
            raise ValueError(f"RA must be in [0, 24) hours, got {self.ra_hours}")
        if not -90 <= self.dec_degrees <= 90:
            raise ValueError(f"DEC must be in [-90, 90] degrees, got {self.dec_degrees}")


# Bright-sky catalog for voice/agent targets (expand over time).
OBJECT_CATALOG: dict[str, EquatorialCoord] = {
    "M31": EquatorialCoord(ra_hours=0.712, dec_degrees=41.269),  # Andromeda
    "M42": EquatorialCoord(ra_hours=5.588, dec_degrees=-5.391),  # Orion Nebula
    "M45": EquatorialCoord(ra_hours=3.791, dec_degrees=24.117),  # Pleiades
    "M13": EquatorialCoord(ra_hours=16.695, dec_degrees=36.460),  # Hercules cluster
    "M57": EquatorialCoord(ra_hours=18.887, dec_degrees=33.029),  # Ring Nebula
    "M51": EquatorialCoord(ra_hours=13.498, dec_degrees=47.195),  # Whirlpool
    "M81": EquatorialCoord(ra_hours=9.928, dec_degrees=69.065),  # Bode's Galaxy
    "M82": EquatorialCoord(ra_hours=9.928, dec_degrees=69.680),  # Cigar Galaxy
    "Jupiter": EquatorialCoord(ra_hours=12.0, dec_degrees=15.0),  # placeholder — use ephemeris
    "Saturn": EquatorialCoord(ra_hours=14.0, dec_degrees=10.0),  # placeholder — use ephemeris
}

_HMS_PATTERN = re.compile(
    r"^\s*(\d{1,2})[h:\s](\d{1,2})[m:\s]?(\d{1,2}(?:\.\d+)?)s?\s*$",
    re.IGNORECASE,
)
_DMS_PATTERN = re.compile(
    r"^([+-]?)(\d{1,2})[d°:\s](\d{1,2})[m':\s]?(\d{1,2}(?:\.\d+)?)\s*$",
    re.IGNORECASE,
)


def parse_ra(ra: str | float) -> float:
    """Parse RA to decimal hours. Accepts float or 'HH:MM:SS' / 'HHhMMmSSs'."""
    if isinstance(ra, (int, float)):
        return float(ra)

    ra = ra.strip()
    if ":" in ra:
        parts = ra.split(":")
        if len(parts) != 3:
            raise ValueError(f"Invalid RA format: {ra}")
        h, m, s = (float(p) for p in parts)
        return h + m / 60 + s / 3600

    match = _HMS_PATTERN.match(ra)
    if match:
        h, m, s = (float(g) for g in match.groups())
        return h + m / 60 + s / 3600

    return float(ra)


def parse_dec(dec: str | float) -> float:
    """Parse DEC to decimal degrees. Accepts float or '±DD:MM:SS'."""
    if isinstance(dec, (int, float)):
        return float(dec)

    dec = dec.strip()
    if ":" in dec:
        sign = -1 if dec.startswith("-") else 1
        parts = dec.lstrip("+-").split(":")
        if len(parts) != 3:
            raise ValueError(f"Invalid DEC format: {dec}")
        d, m, s = (float(p) for p in parts)
        return sign * (d + m / 60 + s / 3600)

    match = _DMS_PATTERN.match(dec)
    if match:
        sign_str, d, m, s = match.groups()
        sign = -1 if sign_str == "-" else 1
        return sign * (float(d) + float(m) / 60 + float(s) / 3600)

    return float(dec)


def resolve_target(name_or_ra: str, dec: str | float | None = None) -> EquatorialCoord:
    """Resolve a catalog name or explicit coordinates to EquatorialCoord."""
    if dec is not None:
        return EquatorialCoord(ra_hours=parse_ra(name_or_ra), dec_degrees=parse_dec(dec))

    key = name_or_ra.strip().upper().replace(" ", "")
    if key in OBJECT_CATALOG:
        return OBJECT_CATALOG[key]

    # Try "RA DEC" as two tokens
    parts = name_or_ra.split()
    if len(parts) == 2:
        return EquatorialCoord(ra_hours=parse_ra(parts[0]), dec_degrees=parse_dec(parts[1]))

    raise ValueError(f"Unknown target: {name_or_ra!r}. Known objects: {sorted(OBJECT_CATALOG)}")