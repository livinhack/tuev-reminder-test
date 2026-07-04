#!/usr/bin/env python3
"""Validate the r028 Manager API foundation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise SystemExit(f"r028 manager API foundation check failed: {message}")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
if manifest.get("version") != "0.1.0-r047":
    fail("manifest version must be 0.1.0-r028")

if read("REMINDER_VERSION.txt").strip() != "r047":
    fail("REMINDER_VERSION.txt must be r028")

init_py = read("custom_components/tuev_reminder/__init__.py")
manager_py = read("custom_components/tuev_reminder/manager.py")
manager_api_py = read("custom_components/tuev_reminder/manager_api.py")

required_manager_functions = [
    "def vehicle_records(",
    "def vehicle_record_by_entry_id(",
    "def vehicle_record_from_entry(",
    "def manager_metadata(",
    "MANAGER_API_VERSION = 3",
    "\"write_api\": True",
    "\"manager_panel_ready\":",
]
for marker in required_manager_functions:
    if marker not in manager_py:
        fail(f"manager.py missing marker: {marker}")

required_ws_markers = [
    'WS_TYPE_METADATA = "tuev_reminder/manager/metadata"',
    'WS_TYPE_VEHICLES_LIST = "tuev_reminder/manager/vehicles/list"',
    'WS_TYPE_VEHICLE_GET = "tuev_reminder/manager/vehicles/get"',
    "websocket_api.async_register_command(hass, websocket_manager_metadata)",
    "websocket_api.async_register_command(hass, websocket_manager_vehicles_list)",
    "websocket_api.async_register_command(hass, websocket_manager_vehicle_get)",
]
for marker in required_ws_markers:
    if marker not in manager_api_py:
        fail(f"manager_api.py missing marker: {marker}")

if "async_register_manager_api(hass)" not in init_py:
    fail("__init__.py must register the Manager WebSocket API")
if "MANAGER_API_REGISTERED_KEY" not in init_py:
    fail("__init__.py must guard against duplicate Manager API registration")

for relative in [
    "docs/REMINDER_R028_MANAGER_API_FOUNDATION.md",
    "docs/COMPAT_CARD_B355_REMINDER_R028.md",
]:
    if not (ROOT / relative).exists():
        fail(f"missing documentation file: {relative}")

print("r028 manager API foundation OK")
