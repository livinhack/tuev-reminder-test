#!/usr/bin/env python3
"""Validate r043 Sidebar three-dot action menu shell."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
PANEL_PY = ROOT / "custom_components" / "tuev_reminder" / "panel.py"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"


def fail(message: str) -> None:
    raise SystemExit(f"r043 three-dot action menu check failed: {message}")


def main() -> None:
    panel = PANEL.read_text(encoding="utf-8")
    panel_py = PANEL_PY.read_text(encoding="utf-8")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if manifest.get("version") != "0.1.0-r043":
        fail("manifest version must be 0.1.0-r043")
    if VERSION.read_text(encoding="utf-8").strip() != "r043":
        fail("REMINDER_VERSION.txt must be r043")

    for marker in [
        "this._openMenuIndex",
        "_openRowMenu(index)",
        "_handleRowAction(action, vehicle)",
        "row-action-menu",
        'data-row-action="edit"',
        'data-row-action="delete"',
        ">Bearbeiten<",
        ">Löschen<",
        "Löschen ist als Menüpunkt vorbereitet",
        "Drei-Punkte-Menü vorbereitet",
    ]:
        if marker not in panel:
            fail(f"panel JS missing {marker!r}")

    if '"mode": "vehicle_list_create_form_action_menu"' not in panel_py:
        fail("panel.py mode should describe the three-dot action menu UI")

    for forbidden in ["tuev-card", "confirm_passed", "set_due_date", "vehicles/update", "vehicles/delete"]:
        if forbidden in panel:
            fail(f"panel JS must not include {forbidden!r}")

    print("r043 three-dot action menu check OK")


if __name__ == "__main__":
    main()
