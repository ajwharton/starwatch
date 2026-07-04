"""Shared test fixtures."""

import pytest

from starwatch.client.mock import MockIndiClient
from starwatch.telescope.controller import TelescopeController


@pytest.fixture
def mock_client() -> MockIndiClient:
    client = MockIndiClient(slew_delay=0)
    client.connect()
    client.unpark()
    return client


@pytest.fixture
def controller(mock_client: MockIndiClient) -> TelescopeController:
    return TelescopeController(mock_client)