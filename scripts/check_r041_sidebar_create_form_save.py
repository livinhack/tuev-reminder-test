#!/usr/bin/env python3
"""Validate r053 Sidebar create form save wiring."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
PANEL_PY = ROOT / "custom_components" / "tuev_reminder" / "panel.py"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"


def fail(message: str) -> None:
    raise SystemExit(f"r053 create form save check failed: {message}")


def main() -> None:
    panel = PANEL.read_text(encoding="utf-8")
    panel_py = PANEL_PY.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if manifest.get("version") != "0.1.0-r060":
        fail("manifest version must be 0.1.0-r060")
    if VERSION.read_text(encoding="utf-8").strip() != "r060":
        fail("REMINDER_VERSION.txt must be r053")

    for marker in [
        "_formPayload()",
        "async _saveCreateForm()",
        'type: "tuev_reminder/manager/vehicles/create"',
        "vehicle: this._formPayload()",
        'id="save-create"',
        "Speichert …",
        "Speicherbereit",
        "result?.vehicles",
        "this._vehicles = result.vehicles",
    ]:
        if marker not in panel:
            fail(f"panel JS missing {marker!r}")

    for stale in [
        "UI-Speichern folgt später",
        "Dieser Stand hält den Speichern-Button noch deaktiviert",
    ]:
        if stale in panel:
            fail(f"panel JS still contains stale disabled-save marker {stale!r}")

    if '"mode": "vehicle_list_create_form_save"' not in panel_py:
        fail("panel.py mode should describe the save-wired UI")

    for forbidden in ["tuev-card", "confirm_passed", "set_due_date"]:
        if forbidden in panel:
            fail(f"panel JS must not include {forbidden!r}")

    print("r053 create form save check OK")


if __name__ == "__main__":
    main()
