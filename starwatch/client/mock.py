"""Mock INDI client for development and testing without hardware."""

from __future__ import annotations

import time

from starwatch.client.base import (
    ConnectionState,
    IndiClientBase,
    SlewState,
    TelescopeStatus,
)
from starwatch.telescope.coordinates import EquatorialCoord


class MockIndiClient(IndiClientBase):
    """Simulates a Celestron mount for local dev and CI."""

    def __init__(self, device_name: str = "Celestron AUX", slew_delay: float = 0.05) -> None:
        self.device_name = device_name
        self.slew_delay = slew_delay
        self._connected = False
        self._tracking = False
        self._parked = True
        self._slew_state = SlewState.PARKED
        self._ra: float | None = None
        self._dec: float | None = None
        self._last_message: str | None = None

    def connect(self) -> bool:
        self._connected = True
        self._last_message = "Connected to mock INDI server"
        return True

    def disconnect(self) -> None:
        self._connected = False
        self._slew_state = SlewState.IDLE
        self._last_message = "Disconnected"

    def is_connected(self) -> bool:
        return self._connected

    def get_status(self) -> TelescopeStatus:
        conn = ConnectionState.CONNECTED if self._connected else ConnectionState.DISCONNECTED
        return TelescopeStatus(
            connection=conn,
            slew=self._slew_state,
            ra_hours=self._ra,
            dec_degrees=self._dec,
            altitude=None,
            azimuth=None,
            tracking=self._tracking,
            parked=self._parked,
            device_name=self.device_name,
            message=self._last_message,
        )

    def slew_to(self, coord: EquatorialCoord) -> None:
        self._require_connected()
        if self._parked:
            raise RuntimeError("Telescope is parked — unpark first")

        self._slew_state = SlewState.SLEWING
        self._last_message = f"Slewing to RA={coord.ra_hours:.4f} DEC={coord.dec_degrees:.4f}"
        time.sleep(self.slew_delay)
        self._ra = coord.ra_hours
        self._dec = coord.dec_degrees
        self._slew_state = SlewState.TRACKING if self._tracking else SlewState.IDLE

    def sync(self, coord: EquatorialCoord) -> None:
        self._require_connected()
        self._ra = coord.ra_hours
        self._dec = coord.dec_degrees
        self._last_message = f"Synced to RA={coord.ra_hours:.4f} DEC={coord.dec_degrees:.4f}"

    def set_tracking(self, enabled: bool) -> None:
        self._require_connected()
        self._tracking = enabled
        if enabled and not self._parked and self._ra is not None:
            self._slew_state = SlewState.TRACKING
        elif not enabled and self._slew_state == SlewState.TRACKING:
            self._slew_state = SlewState.IDLE
        self._last_message = f"Tracking {'enabled' if enabled else 'disabled'}"

    def park(self) -> None:
        self._require_connected()
        self._slew_state = SlewState.PARKING
        time.sleep(self.slew_delay)
        self._parked = True
        self._tracking = False
        self._slew_state = SlewState.PARKED
        self._last_message = "Telescope parked"

    def unpark(self) -> None:
        self._require_connected()
        self._parked = False
        self._slew_state = SlewState.IDLE
        self._last_message = "Telescope unparked"

    def abort(self) -> None:
        self._require_connected()
        if self._slew_state == SlewState.SLEWING:
            self._slew_state = SlewState.IDLE
            self._last_message = "Slew aborted"

    def _require_connected(self) -> None:
        if not self._connected:
            raise RuntimeError("Not connected to INDI server")