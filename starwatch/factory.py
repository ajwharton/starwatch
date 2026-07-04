"""Client factory — selects mock or real INDI backend."""

from __future__ import annotations

from starwatch.client.base import IndiClientBase
from starwatch.client.mock import MockIndiClient
from starwatch.config import StarwatchConfig


def create_client(config: StarwatchConfig) -> IndiClientBase:
    """Instantiate the appropriate INDI client for the configured mode."""
    if config.mode == "mock":
        return MockIndiClient(device_name=config.indi.device_name)

    from starwatch.client.indi import PyIndiClient

    return PyIndiClient(
        host=config.indi.host,
        port=config.indi.port,
        device_name=config.indi.device_name,
    )