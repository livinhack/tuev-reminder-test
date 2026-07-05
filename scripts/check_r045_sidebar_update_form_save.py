#!/usr/bin/env python3
"""Validate r053 Sidebar edit/update save wiring."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")

def fail(message: str) -> None:
    raise SystemExit(f"r053 sidebar update form save check failed: {message}")

def main() -> None:
    manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
    if manifest.get("version") != "0.1.0-r081":
        fail("manifest version must be 0.1.0-r081")
    if read("REMINDER_VERSION.txt").strip() != "r081":
        fail("REMINDER_VERSION.txt must be r053")

    panel = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")
    manager_api = read("custom_components/tuev_reminder/manager_api.py")
    handover = read("HANDOVER.md")

    for marker in [
        "async _saveUpdateForm()",
        'this._view !== "detail"',
        'type: "tuev_reminder/manager/vehicles/update"',
        "entry_id: this._selectedVehicle.entry_id",
        "vehicle: this._formPayload()",
        'id="save-update"',
        "this._applySaveResult(result)",
        "Bestehende Reminder-Entität bearbeiten",
        "Erstellen und Bearbeiten laufen über die Reminder-eigene WebSocket-API",
    ]:
        if marker not in panel:
            fail(f"panel JS missing {marker!r}")

    if "Bearbeiten folgt später" in panel:
        fail("panel still contains disabled edit placeholder")
    if "Bestehende Fahrzeuge bleiben in diesem Stand noch read-only" in panel:
        fail("panel still claims existing vehicles are read-only")

    for marker in [
        'WS_TYPE_VEHICLE_UPDATE = "tuev_reminder/manager/vehicles/update"',
        "def websocket_manager_vehicle_update(",
        "await hass.config_entries.async_reload(entry.entry_id)",
    ]:
        if marker not in manager_api:
            fail(f"manager_api.py missing {marker!r}")

    for forbidden in ["tuev-card", "confirm_passed", "set_due_date"]:
        if forbidden in panel:
            fail(f"panel JS must not include {forbidden!r}")

    if "No Card repository files" not in handover:
        fail("handover must preserve Reminder/Card separation")

    print("r053 sidebar update form save check OK")

if __name__ == "__main__":
    main()
