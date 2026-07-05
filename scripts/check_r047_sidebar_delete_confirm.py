#!/usr/bin/env python3
"""Validate r053 Sidebar delete confirm flow."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")

def fail(message: str) -> None:
    raise SystemExit(f"r053 sidebar delete confirm check failed: {message}")

manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
if manifest.get("version") != "0.1.0-r092":
    fail("manifest version must be 0.1.0-r092")
if read("REMINDER_VERSION.txt").strip() != "r092":
    fail("REMINDER_VERSION.txt must be r053")

manager = read("custom_components/tuev_reminder/manager.py")
api = read("custom_components/tuev_reminder/manager_api.py")
panel = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")

def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle}")

require(api, 'WS_TYPE_VEHICLE_DELETE = "tuev_reminder/manager/vehicles/delete"', "delete websocket type")
require(api, "async def websocket_manager_vehicle_delete", "delete websocket handler")
require(api, "await hass.config_entries.async_remove(entry.entry_id)", "config entry removal")
require(api, "websocket_api.async_register_command(hass, websocket_manager_vehicle_delete)", "delete websocket registration")
require(manager, '"api_version": MANAGER_API_VERSION', "metadata api version")
require(manager, '"write_api_version": 5', "write api version")
require(manager, '"tuev_reminder/manager/vehicles/delete"', "metadata delete command")
require(panel, '_openDeleteConfirm(vehicle)', "delete confirm opener")
require(panel, 'type: "tuev_reminder/manager/vehicles/delete"', "frontend delete websocket call")
require(panel, 'id="confirm-delete"', "confirm delete button")
require(panel, 'Fahrzeug löschen', "delete dialog title")
require(panel, 'Die getrennte Card-Konfiguration wird nicht verändert.', "card separation delete note")

print("r053 sidebar delete confirm check OK")
