"""WebSocket API foundation for the TÜV Reminder Manager UI."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .const import CONF_VEHICLE_NAME
from .manager import (
    entry_title_from_vehicle_values,
    manager_metadata,
    merged_entry_values,
    plate_parts_from_values,
    validate_and_normalize_vehicle_payload,
    vehicle_record_by_entry_id,
    vehicle_records,
)

WS_TYPE_METADATA = "tuev_reminder/manager/metadata"
WS_TYPE_VEHICLES_LIST = "tuev_reminder/manager/vehicles/list"
WS_TYPE_VEHICLE_GET = "tuev_reminder/manager/vehicles/get"
WS_TYPE_VEHICLE_CREATE = "tuev_reminder/manager/vehicles/create"
WS_TYPE_VEHICLE_UPDATE = "tuev_reminder/manager/vehicles/update"
WS_TYPE_VEHICLE_DELETE = "tuev_reminder/manager/vehicles/delete"


def _duplicate_vehicle_errors(
    hass: HomeAssistant,
    normalized: dict,
    *,
    current_entry_id: str | None = None,
) -> list[str]:
    """Return duplicate errors for manager create/update payloads.

    The Sidebar Manager writes normal ConfigEntries. Duplicate checks therefore
    happen in the backend as the source of truth, not only in the panel.
    """
    errors: list[str] = []
    wanted_name = str(normalized.get(CONF_VEHICLE_NAME, "") or "").strip().casefold()
    wanted_plate = str(
        plate_parts_from_values(normalized).get("plate_display", "") or ""
    ).strip().casefold()

    for entry in hass.config_entries.async_entries(DOMAIN):
        if current_entry_id and entry.entry_id == current_entry_id:
            continue
        values = merged_entry_values(entry)
        existing_name = str(values.get(CONF_VEHICLE_NAME, entry.title) or "").strip().casefold()
        existing_plate = str(
            plate_parts_from_values(values).get("plate_display", "") or ""
        ).strip().casefold()
        if wanted_name and existing_name == wanted_name:
            errors.append("Ein Fahrzeug mit diesem Namen existiert bereits.")
        if wanted_plate and existing_plate == wanted_plate:
            errors.append("Ein Fahrzeug mit diesem Kennzeichen existiert bereits.")

    return errors


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


@websocket_api.websocket_command(
    {
        vol.Required("type"): WS_TYPE_VEHICLE_CREATE,
        vol.Required("vehicle"): dict,
    }
)
@websocket_api.async_response
async def websocket_manager_vehicle_create(hass: HomeAssistant, connection, msg) -> None:
    """Create a TÜV Reminder vehicle ConfigEntry from manager form data."""
    errors, normalized = validate_and_normalize_vehicle_payload(msg.get("vehicle") or {})
    errors.extend(_duplicate_vehicle_errors(hass, normalized))
    if errors:
        connection.send_error(msg["id"], "validation_failed", f"TÜV Reminder vehicle data is invalid: {errors}")
        return

    existing_entry_ids = {entry.entry_id for entry in hass.config_entries.async_entries(DOMAIN)}
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_IMPORT},
        data=normalized,
    )

    if result.get("type") != "create_entry":
        connection.send_error(
            msg["id"],
            "create_failed",
            f"TÜV Reminder ConfigEntry creation did not complete: {result.get('reason') or result.get('type')}",
        )
        return

    created_entry = result.get("result")
    if created_entry is None:
        created_entry = next(
            (
                entry
                for entry in hass.config_entries.async_entries(DOMAIN)
                if entry.entry_id not in existing_entry_ids
            ),
            None,
        )

    record = None
    if created_entry is not None:
        record = vehicle_record_by_entry_id(hass, created_entry.entry_id)

    connection.send_result(
        msg["id"],
        {
            "created": True,
            "vehicle": record,
            "vehicles": vehicle_records(hass),
        },
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): WS_TYPE_VEHICLE_UPDATE,
        vol.Required("entry_id"): str,
        vol.Required("vehicle"): dict,
    }
)
@websocket_api.async_response
async def websocket_manager_vehicle_update(hass: HomeAssistant, connection, msg) -> None:
    """Update an existing TÜV Reminder vehicle ConfigEntry from manager form data."""
    entry = hass.config_entries.async_get_entry(msg["entry_id"])
    if entry is None or entry.domain != DOMAIN:
        connection.send_error(msg["id"], "not_found", "TÜV Reminder vehicle not found")
        return

    errors, normalized = validate_and_normalize_vehicle_payload(msg.get("vehicle") or {})
    errors.extend(_duplicate_vehicle_errors(hass, normalized, current_entry_id=entry.entry_id))
    if errors:
        connection.send_error(msg["id"], "validation_failed", f"TÜV Reminder vehicle data is invalid: {errors}")
        return

    hass.config_entries.async_update_entry(
        entry,
        title=entry_title_from_vehicle_values(normalized),
        options=normalized,
    )
    await hass.config_entries.async_reload(entry.entry_id)

    connection.send_result(
        msg["id"],
        {
            "updated": True,
            "vehicle": vehicle_record_by_entry_id(hass, entry.entry_id),
            "vehicles": vehicle_records(hass),
        },
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): WS_TYPE_VEHICLE_DELETE,
        vol.Required("entry_id"): str,
    }
)
@websocket_api.async_response
async def websocket_manager_vehicle_delete(hass: HomeAssistant, connection, msg) -> None:
    """Delete an existing TÜV Reminder vehicle ConfigEntry from the manager UI."""
    entry = hass.config_entries.async_get_entry(msg["entry_id"])
    if entry is None or entry.domain != DOMAIN:
        connection.send_error(msg["id"], "not_found", "TÜV Reminder vehicle not found")
        return

    await hass.config_entries.async_remove(entry.entry_id)

    connection.send_result(
        msg["id"],
        {
            "deleted": True,
            "entry_id": msg["entry_id"],
            "vehicles": vehicle_records(hass),
        },
    )


def async_register_manager_api(hass: HomeAssistant) -> None:
    """Register the manager WebSocket API commands once."""
    websocket_api.async_register_command(hass, websocket_manager_metadata)
    websocket_api.async_register_command(hass, websocket_manager_vehicles_list)
    websocket_api.async_register_command(hass, websocket_manager_vehicle_get)
    websocket_api.async_register_command(hass, websocket_manager_vehicle_create)
    websocket_api.async_register_command(hass, websocket_manager_vehicle_update)
    websocket_api.async_register_command(hass, websocket_manager_vehicle_delete)
