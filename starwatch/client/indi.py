"""Real PyIndi client — only available when pyindi-client is installed (Pi/StellarMate)."""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from starwatch.client.base import (
    ConnectionState,
    IndiClientBase,
    SlewState,
    TelescopeStatus,
)
from starwatch.telescope.coordinates import EquatorialCoord

logger = logging.getLogger(__name__)

try:
    import PyIndi  # type: ignore[import-untyped]

    _PYINDI_AVAILABLE = True
except ImportError:
    _PYINDI_AVAILABLE = False
    if TYPE_CHECKING:
        import PyIndi  # noqa: F401


class _IndiEventClient(PyIndi.BaseClient if _PYINDI_AVAILABLE else object):  # type: ignore[misc,name-defined]
    """Thin INDI event handler — collects property updates."""

    def __init__(self) -> None:
        if _PYINDI_AVAILABLE:
            super().__init__()
        self.devices: dict[str, object] = {}
        self.messages: list[str] = []

    def newDevice(self, device) -> None:  # noqa: N802
        self.devices[device.getDeviceName()] = device

    def newMessage(self, device, message_index) -> None:  # noqa: N802
        self.messages.append(device.messageQueue(message_index))


class PyIndiClient(IndiClientBase):
    """Production INDI client for Celestron AUX / NexStar Evolution."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 7624,
        device_name: str = "Celestron AUX",
        connect_timeout: float = 5.0,
    ) -> None:
        if not _PYINDI_AVAILABLE:
            raise ImportError(
                "pyindi-client is not installed. "
                "Install with: pip install 'starwatch[indi]' on your Pi/StellarMate."
            )
        self.host = host
        self.port = port
        self.device_name = device_name
        self.connect_timeout = connect_timeout
        self._client = _IndiEventClient()
        self._client.setServer(host, port)

    def connect(self) -> bool:
        if not self._client.connectServer():
            return False
        deadline = time.monotonic() + self.connect_timeout
        while time.monotonic() < deadline:
            if self._client.getDevice(self.device_name):
                return True
            time.sleep(0.2)
        logger.warning("Connected to INDI but device %s not found", self.device_name)
        return True  # server up; device may appear after profile load

    def disconnect(self) -> None:
        self._client.disconnectServer()

    def is_connected(self) -> bool:
        return self._client.isServerConnected()

    def _device(self):
        dev = self._client.getDevice(self.device_name)
        if dev is None:
            raise RuntimeError(f"INDI device {self.device_name!r} not available")
        return dev

    def get_status(self) -> TelescopeStatus:
        conn = (
            ConnectionState.CONNECTED
            if self.is_connected()
            else ConnectionState.DISCONNECTED
        )
        if not self.is_connected():
            return TelescopeStatus(
                connection=conn,
                slew=SlewState.IDLE,
                ra_hours=None,
                dec_degrees=None,
                altitude=None,
                azimuth=None,
                tracking=False,
                parked=False,
                device_name=self.device_name,
            )

        dev = self._device()
        ra, dec, alt, az = None, None, None, None
        tracking = False
        parked = False
        slew = SlewState.IDLE

        try:
            coord_prop = dev.getNumber("EQUATORIAL_EOD_COORD")
            if coord_prop:
                ra = coord_prop[0].getValue()
                dec = coord_prop[1].getValue()
        except Exception:
            pass

        try:
            track_prop = dev.getSwitch("TELESCOPE_TRACK_STATE")
            if track_prop:
                tracking = track_prop[0].getState() == PyIndi.ISS_ON
        except Exception:
            pass

        try:
            park_prop = dev.getSwitch("TELESCOPE_PARK")
            if park_prop:
                parked = park_prop[0].getState() == PyIndi.ISS_ON
                if parked:
                    slew = SlewState.PARKED
        except Exception:
            pass

        try:
            slew_prop = dev.getLight("TELESCOPE_SLEW")
            if slew_prop:
                state = slew_prop[0].getState()
                if state == PyIndi.IPS_BUSY:
                    slew = SlewState.SLEWING
                elif tracking:
                    slew = SlewState.TRACKING
        except Exception:
            if tracking:
                slew = SlewState.TRACKING

        msg = self._client.messages[-1] if self._client.messages else None
        return TelescopeStatus(
            connection=conn,
            slew=slew,
            ra_hours=ra,
            dec_degrees=dec,
            altitude=alt,
            azimuth=az,
            tracking=tracking,
            parked=parked,
            device_name=self.device_name,
            message=msg,
        )

    def slew_to(self, coord: EquatorialCoord) -> None:
        dev = self._device()
        coords = dev.getNumber("EQUATORIAL_EOD_COORD")
        coords[0].setValue(coord.ra_hours)
        coords[1].setValue(coord.dec_degrees)
        self._client.sendNewNumber(coords)

    def sync(self, coord: EquatorialCoord) -> None:
        dev = self._device()
        coords = dev.getNumber("EQUATORIAL_EOD_COORD")
        coords[0].setValue(coord.ra_hours)
        coords[1].setValue(coord.dec_degrees)
        self._client.sendNewNumber(coords)
        # INDI sync uses ON_COORD_SET sync mode — set via property if available
        try:
            mode = dev.getSwitch("ON_COORD_SET")
            for i in range(mode.nsp):
                mode[i].setState(PyIndi.ISS_OFF)
            sync_widget = mode.findWidgetByName("SYNC")
            if sync_widget:
                sync_widget.setState(PyIndi.ISS_ON)
                self._client.sendNewSwitch(mode)
        except Exception:
            logger.debug("ON_COORD_SET not available — sync sent as coord update")

    def set_tracking(self, enabled: bool) -> None:
        dev = self._device()
        track = dev.getSwitch("TELESCOPE_TRACK_STATE")
        track[0].setState(PyIndi.ISS_ON if enabled else PyIndi.ISS_OFF)
        track[1].setState(PyIndi.ISS_OFF if enabled else PyIndi.ISS_ON)
        self._client.sendNewSwitch(track)

    def park(self) -> None:
        dev = self._device()
        park = dev.getSwitch("TELESCOPE_PARK")
        park[0].setState(PyIndi.ISS_ON)
        park[1].setState(PyIndi.ISS_OFF)
        self._client.sendNewSwitch(park)

    def unpark(self) -> None:
        dev = self._device()
        park = dev.getSwitch("TELESCOPE_PARK")
        park[0].setState(PyIndi.ISS_OFF)
        park[1].setState(PyIndi.ISS_ON)
        self._client.sendNewSwitch(park)

    def abort(self) -> None:
        dev = self._device()
        try:
            abort = dev.getSwitch("TELESCOPE_ABORT_MOTION")
            abort[0].setState(PyIndi.ISS_ON)
            self._client.sendNewSwitch(abort)
        except Exception:
            logger.warning("TELESCOPE_ABORT_MOTION not available on %s", self.device_name)