"""Tests for telescope controller and mock client."""

import pytest

from starwatch.client.mock import MockIndiClient
from starwatch.telescope.controller import TelescopeController, TrackingMode


class TestMockClient:
    def test_connect_disconnect(self):
        client = MockIndiClient()
        assert client.connect()
        assert client.is_connected()
        client.disconnect()
        assert not client.is_connected()

    def test_park_unpark(self):
        client = MockIndiClient()
        client.connect()
        assert client.get_status().parked
        client.unpark()
        assert not client.get_status().parked
        client.park()
        assert client.get_status().parked

    def test_slew_while_parked_fails(self):
        client = MockIndiClient()
        client.connect()
        ctrl = TelescopeController(client)
        with pytest.raises(RuntimeError, match="parked"):
            ctrl.slew_to_target("M31")


class TestController:
    def test_slew_to_m31(self, controller: TelescopeController):
        coord = controller.slew_to_target("M31")
        assert coord.ra_hours == pytest.approx(0.712)
        status = controller.get_state().status
        assert status.ra_hours == pytest.approx(0.712)
        assert not status.parked

    def test_tracking(self, controller: TelescopeController):
        controller.set_tracking(TrackingMode.SIDEREAL)
        assert controller.get_state().status.tracking
        controller.set_tracking(TrackingMode.OFF)
        assert not controller.get_state().status.tracking

    def test_park_after_session(self, controller: TelescopeController):
        controller.slew_to_target("M42")
        controller.park()
        assert controller.get_state().status.parked
        assert not controller.get_state().status.tracking

    def test_abort(self, mock_client: MockIndiClient):
        mock_client._slew_state = mock_client._slew_state  # ensure connected
        from starwatch.client.base import SlewState

        mock_client._slew_state = SlewState.SLEWING
        mock_client.abort()
        assert mock_client.get_status().slew == SlewState.IDLE