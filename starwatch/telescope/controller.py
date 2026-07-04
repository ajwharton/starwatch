"""High-level telescope controller used by API and agents."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from starwatch.client.base import IndiClientBase, TelescopeStatus
from starwatch.telescope.coordinates import EquatorialCoord, resolve_target


class TrackingMode(str, Enum):
    OFF = "off"
    SIDEREAL = "sidereal"


@dataclass
class TelescopeState:
    status: TelescopeStatus
    target: str | None = None


class TelescopeController:
    """Orchestrates telescope operations with safety checks."""

    def __init__(self, client: IndiClientBase) -> None:
        self._client = client

    @property
    def client(self) -> IndiClientBase:
        return self._client

    def connect(self) -> bool:
        return self._client.connect()

    def disconnect(self) -> None:
        self._client.disconnect()

    def get_state(self) -> TelescopeState:
        return TelescopeState(status=self._client.get_status())

    def slew_to_target(self, target: str, dec: str | float | None = None) -> EquatorialCoord:
        """Resolve target name or coordinates and slew."""
        coord = resolve_target(target, dec)
        self._ensure_ready_to_slew()
        self._client.slew_to(coord)
        return coord

    def slew_to_coords(self, ra: str | float, dec: str | float) -> EquatorialCoord:
        """Slew to explicit RA/DEC."""
        coord = resolve_target(str(ra), dec)
        self._ensure_ready_to_slew()
        self._client.slew_to(coord)
        return coord

    def sync_to_target(self, target: str, dec: str | float | None = None) -> EquatorialCoord:
        coord = resolve_target(target, dec)
        self._client.sync(coord)
        return coord

    def set_tracking(self, mode: TrackingMode) -> None:
        self._client.set_tracking(mode == TrackingMode.SIDEREAL)

    def park(self) -> None:
        self._client.park()

    def unpark(self) -> None:
        self._client.unpark()

    def abort(self) -> None:
        self._client.abort()

    def _ensure_ready_to_slew(self) -> None:
        status = self._client.get_status()
        if not self._client.is_connected():
            raise RuntimeError("Not connected to telescope")
        if status.parked:
            raise RuntimeError("Telescope is parked — call unpark first")