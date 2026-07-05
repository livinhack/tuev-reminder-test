#!/usr/bin/env python3
"""Validate r053 Backend Update API foundation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise SystemExit(f"r053 backend update API check failed: {message}")


def main() -> None:
    manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
    if manifest.get("version") != "0.1.0-r098":
        fail("manifest version must be 0.1.0-r098")
    if read("REMINDER_VERSION.txt").strip() != "r098":
        fail("REMINDER_VERSION.txt must be r053")

    manager = read("custom_components/tuev_reminder/manager.py")
    manager_api = read("custom_components/tuev_reminder/manager_api.py")
    panel = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")
    handover = read("HANDOVER.md")

    for marker in [
        "MANAGER_API_VERSION = 5",
        '"write_api_version": 5',
        '"tuev_reminder/manager/vehicles/create"',
        '"tuev_reminder/manager/vehicles/update"',
    ]:
        if marker not in manager:
            fail(f"manager.py missing {marker!r}")

    for marker in [
        'WS_TYPE_VEHICLE_UPDATE = "tuev_reminder/manager/vehicles/update"',
        "def websocket_manager_vehicle_update(",
        "validate_and_normalize_vehicle_payload(msg.get(\"vehicle\") or {})",
        "entry_title_from_vehicle_values(normalized)",
        "hass.config_entries.async_update_entry(",
        "options=normalized",
        "await hass.config_entries.async_reload(entry.entry_id)",
        '"updated": True',
        "websocket_api.async_register_command(hass, websocket_manager_vehicle_update)",
    ]:
        if marker not in manager_api:
            fail(f"manager_api.py missing {marker!r}")

    # Delete is intentionally added after the r044 update foundation.
    if "No Card repository files" not in handover:
        fail("handover must preserve Reminder/Card separation")

    for relative in [
        "docs/REMINDER_R046_BACKEND_UPDATE_API_FOUNDATION.md",
        "docs/COMPAT_CARD_B355_REMINDER_R046.md",
    ]:
        if not (ROOT / relative).exists():
            fail(f"missing documentation file: {relative}")

    print("r053 backend update API check OK")


if __name__ == "__main__":
    main()
