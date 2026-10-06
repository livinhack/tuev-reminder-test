"""Shared fixtures for the TÜV Reminder tests (r115).

Run locally:
    pip install -r requirements_test.txt
    pytest
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant, callback
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

import custom_components.tuev_reminder as integration

pytest_plugins = ["pytest_homeassistant_custom_component"]

DOMAIN = "tuev_reminder"

BASE_VEHICLE = {
    "vehicle_name": "Golf",
    "plate": "TR AB 123",
    "plate_kind": "standard",
    "plate_format": "single_line",
    "plate_suffix_h": False,
    "plate_suffix_e": False,
    "month": 3,
    "year": 2027,
    "interval": 2,
    "reminder_offset_days": 7,
}


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Allow loading custom_components/ in every test."""
    yield


@pytest.fixture
def panel_registration():
    """Capture the Sidebar panel registration instead of needing hass_frontend."""
    with patch(
        "custom_components.tuev_reminder.panel.frontend.async_register_built_in_panel",
        MagicMock(),
    ) as mock_register:
        yield mock_register


@pytest.fixture
async def setup_integration(hass: HomeAssistant, panel_registration):
    """Return a helper that adds vehicle entries and sets up the integration."""

    async def _setup(*vehicles: dict) -> list[MockConfigEntry]:
        entries = []
        for vehicle in vehicles or (BASE_VEHICLE,):
            entry = MockConfigEntry(
                domain=DOMAIN,
                data=dict(vehicle),
                title=vehicle.get("vehicle_name", "Fahrzeug"),
            )
            entry.add_to_hass(hass)
            entries.append(entry)

        assert await async_setup_component(hass, "http", {})
        # frontend/panel_custom need the large hass_frontend package. The
        # panel registration itself is captured by `panel_registration`.
        hass.config.components.update({"frontend", "panel_custom"})
        assert await async_setup_component(hass, DOMAIN, {})
        await hass.async_block_till_done()
        return entries

    return _setup


def sensor_entity_id(hass: HomeAssistant, entry: MockConfigEntry) -> str:
    from homeassistant.helpers import entity_registry as er

    registry = er.async_get(hass)
    for reg_entry in er.async_entries_for_config_entry(registry, entry.entry_id):
        if reg_entry.domain == "sensor":
            return reg_entry.entity_id
    raise AssertionError("no sensor for entry")


@pytest.fixture
def record_sensor_states(hass: HomeAssistant):
    """Record every state written for sensor entities."""
    states: list[tuple[str, str | None]] = []

    @callback
    def _listener(event):
        if event.data["entity_id"].startswith("sensor."):
            new_state = event.data.get("new_state")
            states.append((event.data["entity_id"], new_state.state if new_state else None))

    hass.bus.async_listen("state_changed", _listener)
    return states


@pytest.fixture
def count_entry_setups():
    """Count how often async_setup_entry runs (i.e. reloads after the first setup)."""
    calls = {"count": 0}
    original = integration.async_setup_entry

    async def _wrapped(hass, entry):
        calls["count"] += 1
        return await original(hass, entry)

    with patch.object(integration, "async_setup_entry", _wrapped):
        yield calls
