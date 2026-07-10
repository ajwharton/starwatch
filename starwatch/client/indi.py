"""Real PyIndi client — only available when pyindi-client is installed (Pi/StellarMate)."""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Any

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
        try:
            name = device.getDeviceName()
            self.devices[name] = device
        except Exception as e:
            logger.debug("newDevice error: %s", e)

    def newMessage(self, device, message_index) -> None:  # noqa: N802
        try:
            self.messages.append(device.messageQueue(message_index))
        except Exception:
            pass

    # Newer INDI may call these; no-op stubs avoid pure-virtual issues
    def newProperty(self, property) -> None:  # noqa: N802
        pass

    def updateProperty(self, property) -> None:  # noqa: N802
        pass

    def removeProperty(self, property) -> None:  # noqa: N802
        pass

    def newBLOB(self, bp) -> None:  # noqa: N802
        pass

    def newSwitch(self, svp) -> None:  # noqa: N802
        pass

    def newNumber(self, nvp) -> None:  # noqa: N802
        pass

    def newText(self, tvp) -> None:  # noqa: N802
        pass

    def newLight(self, lvp) -> None:  # noqa: N802
        pass

    def serverConnected(self) -> None:  # noqa: N802
        pass

    def serverDisconnected(self, exit_code: int) -> None:  # noqa: N802
        pass


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
        try:
            self._client.disconnectServer()
        except Exception:
            pass

    def is_connected(self) -> bool:
        try:
            return bool(self._client.isServerConnected())
        except Exception:
            return False

    def _device(self):
        dev = self._client.getDevice(self.device_name)
        if dev is None:
            raise RuntimeError(f"INDI device {self.device_name!r} not available")
        return dev

    @staticmethod
    def _prop_usable(prop: Any) -> bool:
        """False for None or empty/invalid SWIG property proxies (indexing those can SEGV)."""
        if prop is None:
            return False
        try:
            # SWIG proxies often implement __bool__ as false when invalid
            if not prop:
                return False
        except Exception:
            return False
        try:
            if hasattr(prop, "getCount"):
                n = prop.getCount()
                return bool(n and n > 0)
        except Exception:
            pass
        try:
            return len(prop) > 0
        except Exception:
            return False

    def _wait_prop(self, dev, getter: str, name: str, timeout: float = 3.0) -> Any:
        """Wait for a usable property; return None if missing/invalid (never index empty)."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                prop = getattr(dev, getter)(name)
                if self._prop_usable(prop):
                    return prop
            except Exception:
                pass
            time.sleep(0.15)
        return None

    def _ensure_device_connected(self) -> None:
        """Toggle CONNECTION switch if present (no-op when already connected)."""
        dev = self._device()
        conn = self._wait_prop(dev, "getSwitch", "CONNECTION", timeout=2.0)
        if conn is None:
            return
        try:
            # CONNECT is usually index 0
            if conn[0].getState() != PyIndi.ISS_ON:
                conn[0].setState(PyIndi.ISS_ON)
                if conn.getCount() > 1 or True:
                    try:
                        conn[1].setState(PyIndi.ISS_OFF)
                    except Exception:
                        pass
                self._client.sendNewSwitch(conn)
                time.sleep(0.5)
        except Exception as e:
            logger.warning("Could not set CONNECTION: %s", e)

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

        try:
            dev = self._device()
        except RuntimeError:
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
                message="INDI device not ready",
            )

        ra, dec, alt, az = None, None, None, None
        tracking = False
        parked = False
        slew = SlewState.IDLE

        try:
            coord_prop = self._wait_prop(dev, "getNumber", "EQUATORIAL_EOD_COORD", 0.5)
            if coord_prop is not None:
                ra = coord_prop[0].getValue()
                dec = coord_prop[1].getValue()
        except Exception:
            pass

        try:
            track_prop = self._wait_prop(dev, "getSwitch", "TELESCOPE_TRACK_STATE", 0.3)
            if track_prop is not None:
                tracking = track_prop[0].getState() == PyIndi.ISS_ON
        except Exception:
            pass

        try:
            park_prop = self._wait_prop(dev, "getSwitch", "TELESCOPE_PARK", 0.3)
            if park_prop is not None:
                parked = park_prop[0].getState() == PyIndi.ISS_ON
                if parked:
                    slew = SlewState.PARKED
        except Exception:
            pass

        try:
            if tracking and not parked:
                slew = SlewState.TRACKING
        except Exception:
            pass

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
        self._ensure_device_connected()
        dev = self._device()
        coords = self._wait_prop(dev, "getNumber", "EQUATORIAL_EOD_COORD", 5.0)
        if coords is None:
            raise RuntimeError(
                "EQUATORIAL_EOD_COORD not available — is the mount connected and powered?"
            )
        try:
            mode = self._wait_prop(dev, "getSwitch", "ON_COORD_SET", 1.0)
            if mode is not None:
                for i in range(mode.getCount()):
                    mode[i].setState(PyIndi.ISS_OFF)
                try:
                    w = mode.findWidgetByName("TRACK")
                    if w:
                        w.setState(PyIndi.ISS_ON)
                    else:
                        mode[0].setState(PyIndi.ISS_ON)
                except Exception:
                    mode[0].setState(PyIndi.ISS_ON)
                self._client.sendNewSwitch(mode)
        except Exception as e:
            logger.debug("ON_COORD_SET: %s", e)

        coords[0].setValue(coord.ra_hours)
        coords[1].setValue(coord.dec_degrees)
        self._client.sendNewNumber(coords)

    def sync(self, coord: EquatorialCoord) -> None:
        self._ensure_device_connected()
        dev = self._device()
        try:
            mode = self._wait_prop(dev, "getSwitch", "ON_COORD_SET", 2.0)
            if mode is not None:
                for i in range(mode.getCount()):
                    mode[i].setState(PyIndi.ISS_OFF)
                sync_widget = mode.findWidgetByName("SYNC")
                if sync_widget:
                    sync_widget.setState(PyIndi.ISS_ON)
                    self._client.sendNewSwitch(mode)
        except Exception as e:
            logger.debug("ON_COORD_SET sync: %s", e)

        coords = self._wait_prop(dev, "getNumber", "EQUATORIAL_EOD_COORD", 5.0)
        if coords is None:
            raise RuntimeError("EQUATORIAL_EOD_COORD not available for sync")
        coords[0].setValue(coord.ra_hours)
        coords[1].setValue(coord.dec_degrees)
        self._client.sendNewNumber(coords)

    def set_tracking(self, enabled: bool) -> None:
        self._ensure_device_connected()
        dev = self._device()
        track = self._wait_prop(dev, "getSwitch", "TELESCOPE_TRACK_STATE", 3.0)
        if track is None:
            raise RuntimeError("TELESCOPE_TRACK_STATE not available — mount not ready")
        track[0].setState(PyIndi.ISS_ON if enabled else PyIndi.ISS_OFF)
        try:
            track[1].setState(PyIndi.ISS_OFF if enabled else PyIndi.ISS_ON)
        except Exception:
            pass
        self._client.sendNewSwitch(track)

    def park(self) -> None:
        self._ensure_device_connected()
        dev = self._device()
        park = self._wait_prop(dev, "getSwitch", "TELESCOPE_PARK", 3.0)
        if park is None:
            raise RuntimeError("TELESCOPE_PARK not available — mount not ready")
        park[0].setState(PyIndi.ISS_ON)
        try:
            park[1].setState(PyIndi.ISS_OFF)
        except Exception:
            pass
        self._client.sendNewSwitch(park)

    def unpark(self) -> None:
        self._ensure_device_connected()
        dev = self._device()
        park = self._wait_prop(dev, "getSwitch", "TELESCOPE_PARK", 3.0)
        if park is None:
            raise RuntimeError("TELESCOPE_PARK not available — mount not ready")
        park[0].setState(PyIndi.ISS_OFF)
        try:
            park[1].setState(PyIndi.ISS_ON)
        except Exception:
            pass
        self._client.sendNewSwitch(park)

    def abort(self) -> None:
        dev = self._device()
        abort = self._wait_prop(dev, "getSwitch", "TELESCOPE_ABORT_MOTION", 2.0)
        if abort is None:
            raise RuntimeError("TELESCOPE_ABORT_MOTION not available")
        abort[0].setState(PyIndi.ISS_ON)
        self._client.sendNewSwitch(abort)
