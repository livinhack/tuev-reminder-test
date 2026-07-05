#!/usr/bin/env python3
"""Validate r053 Backend Create API foundation and plain add controls."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise SystemExit(f"r053 backend create API check failed: {message}")


def main() -> None:
    manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
    if manifest.get("version") != "0.1.0-r105":
        fail("manifest version must be 0.1.0-r105")
    if read("REMINDER_VERSION.txt").strip() != "r105":
        fail("REMINDER_VERSION.txt must be r053")

    manager = read("custom_components/tuev_reminder/manager.py")
    manager_api = read("custom_components/tuev_reminder/manager_api.py")
    config_flow = read("custom_components/tuev_reminder/config_flow.py")
    panel = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")
    panel_py = read("custom_components/tuev_reminder/panel.py")

    for marker in [
        "MANAGER_API_VERSION = 5",
        "def validate_and_normalize_vehicle_payload(",
        "def entry_title_from_vehicle_values(",
        '"write_api": True',
        '"write_api_version": 5',
        '"tuev_reminder/manager/vehicles/create"',
    ]:
        if marker not in manager:
            fail(f"manager.py missing {marker!r}")

    for marker in [
        'WS_TYPE_VEHICLE_CREATE = "tuev_reminder/manager/vehicles/create"',
        "def websocket_manager_vehicle_create(",
        "validate_and_normalize_vehicle_payload",
        "hass.config_entries.flow.async_init",
        "config_entries.SOURCE_IMPORT",
        "websocket_api.async_register_command(hass, websocket_manager_vehicle_create)",
    ]:
        if marker not in manager_api:
            fail(f"manager_api.py missing {marker!r}")

    for marker in [
        "async def async_step_import",
        "validate_and_normalize_vehicle_payload(user_input or {})",
        "entry_title_from_vehicle_values(values)",
    ]:
        if marker not in config_flow:
            fail(f"config_flow.py missing {marker!r}")

    for marker in [
        '"mode": "vehicle_list_create_form_save"',
        '"write_api": True',
    ]:
        if marker not in panel_py:
            fail(f"panel.py missing {marker!r}")

    if '<span class="add-label">Neues Fahrzeug</span>' in panel:
        fail("plain plus controls must not render the Neues Fahrzeug label beside add buttons")
    for marker in [
        'data-create-trigger="controls"',
        "list-create-control",
        "button.icon-action",
        "#save-create",
    ]:
        if marker not in panel:
            fail(f"panel JS missing {marker!r}")

    for forbidden in [
        "tuev-card",
        "confirm_passed",
        "set_due_date",
    ]:
        if forbidden in panel:
            fail(f"panel JS must not include {forbidden!r}")

    for relative in [
        "docs/REMINDER_R040_BACKEND_CREATE_API_FOUNDATION.md",
        "docs/COMPAT_CARD_B355_REMINDER_R040.md",
    ]:
        if not (ROOT / relative).exists():
            fail(f"missing documentation file: {relative}")

    print("r053 backend create API check OK")


if __name__ == "__main__":
    main()
