"""WebSocket API foundation for a future TÜV Reminder Manager UI."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant

from .manager import manager_metadata, vehicle_record_by_entry_id, vehicle_records

WS_TYPE_METADATA = "tuev_reminder/manager/metadata"
WS_TYPE_VEHICLES_LIST = "tuev_reminder/manager/vehicles/list"
WS_TYPE_VEHICLE_GET = "tuev_reminder/manager/vehicles/get"


@websocket_api.websocket_command(
    {
        vol.Required("type"): WS_TYPE_METADATA,
    }
)
@websocket_api.async_response
async def websocket_manager_metadata(hass: HomeAssistant, connection, msg) -> None:
    """Return static manager metadata and UI capabilities."""
    connection.send_result(msg["id"], manager_metadata())


@websocket_api.websocket_command(
    {
        vol.Required("type"): WS_TYPE_VEHICLES_LIST,
    }
)
@websocket_api.async_response
async def websocket_manager_vehicles_list(hass: HomeAssistant, connection, msg) -> None:
    """Return all TÜV Reminder vehicles as stable records."""
    connection.send_result(msg["id"], {"vehicles": vehicle_records(hass)})


@websocket_api.websocket_command(
    {
        vol.Required("type"): WS_TYPE_VEHICLE_GET,
        vol.Required("entry_id"): str,
    }
)
@websocket_api.async_response
async def websocket_manager_vehicle_get(hass: HomeAssistant, connection, msg) -> None:
    """Return one TÜV Reminder vehicle by config entry id."""
    record = vehicle_record_by_entry_id(hass, msg["entry_id"])
    if record is None:
        connection.send_error(msg["id"], "not_found", "TÜV Reminder vehicle not found")
        return
    connection.send_result(msg["id"], {"vehicle": record})


def async_register_manager_api(hass: HomeAssistant) -> None:
    """Register the read-only manager WebSocket API commands once."""
    websocket_api.async_register_command(hass, websocket_manager_metadata)
    websocket_api.async_register_command(hass, websocket_manager_vehicles_list)
    websocket_api.async_register_command(hass, websocket_manager_vehicle_get)
