"""Abstract INDI client interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from starwatch.telescope.coordinates import EquatorialCoord


class ConnectionState(str, Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"


class SlewState(str, Enum):
    IDLE = "idle"
    SLEWING = "slewing"
    TRACKING = "tracking"
    PARKED = "parked"
    PARKING = "parking"
    ERROR = "error"


@dataclass
class TelescopeStatus:
    connection: ConnectionState
    slew: SlewState
    ra_hours: float | None
    dec_degrees: float | None
    altitude: float | None
    azimuth: float | None
    tracking: bool
    parked: bool
    device_name: str
    message: str | None = None


class IndiClientBase(ABC):
    """Backend-agnostic telescope control interface."""

    @abstractmethod
    def connect(self) -> bool:
        """Connect to the INDI server."""

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the INDI server."""

    @abstractmethod
    def is_connected(self) -> bool:
        """Return True if connected to INDI server."""

    @abstractmethod
    def get_status(self) -> TelescopeStatus:
        """Return current telescope status."""

    @abstractmethod
    def slew_to(self, coord: EquatorialCoord) -> None:
        """Slew to equatorial coordinates."""

    @abstractmethod
    def sync(self, coord: EquatorialCoord) -> None:
        """Sync mount model to coordinates (after plate solve or bright star)."""

    @abstractmethod
    def set_tracking(self, enabled: bool) -> None:
        """Enable or disable sidereal tracking."""

    @abstractmethod
    def park(self) -> None:
        """Park the telescope."""

    @abstractmethod
    def unpark(self) -> None:
        """Unpark the telescope."""

    @abstractmethod
    def abort(self) -> None:
        """Abort current slew."""