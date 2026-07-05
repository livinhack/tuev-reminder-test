#!/usr/bin/env python3
"""Validate Sidebar create form structure after save wiring."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"


def require(text: str, needle: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing expected marker: {needle}")


def main() -> int:
    js = JS.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert VERSION.read_text(encoding="utf-8").strip() == "r081"
    assert manifest["version"] == "0.1.0-r081"

    require(js, 'this._view = "list"')
    require(js, "_renderCreateForm()")
    require(js, "_openCreateForm()")
    require(js, "Neues Fahrzeug")
    require(js, "Neues Fahrzeug anlegen")
    require(js, "Speichern")
    require(js, "plate_suffix_h")
    require(js, "plate_suffix_e")
    require(js, "change_plate_common_text")
    require(js, "change_plate_vehicle_digit")
    require(js, "season_start_month")
    require(js, "season_end_month")
    require(js, "write_api")

    forbidden = [
        "confirm_passed",
        "set_due_date",
        "tuev-card",
        "hui-",
        "lovelace",
    ]
    for needle in forbidden:
        if needle in js:
            raise AssertionError(f"r053 Sidebar form skeleton must not include {needle!r}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
