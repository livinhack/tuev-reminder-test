#!/usr/bin/env python3
"""Validate r053 Sidebar responsive table width fix."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"


def fail(message: str) -> None:
    raise SystemExit(f"r053 sidebar responsive table width check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("version") != "0.1.0-r100":
        fail("manifest version must be 0.1.0-r100")
    if VERSION.read_text(encoding="utf-8").strip() != "r100":
        fail("REMINDER_VERSION.txt must be r053")

    panel = PANEL.read_text(encoding="utf-8")
    require(panel, "@media (max-width: 1100px)", "narrow/mobile landscape table media query")
    require(panel, ".manager-table {", "manager table css")
    require(panel, "min-width: 0;", "mobile min-width reset")
    require(panel, "table-layout: fixed;", "fixed mobile table layout")
    require(panel, ".col-preview, .preview-cell { display: none; }", "mobile preview column hide")
    require(panel, ".mobile-plate-slot", "mobile plate text fallback")
    require(panel, "@media (max-width: 460px)", "very narrow media query")
    require(panel, ".col-reminder, .reminder-cell { display: none; }", "very narrow reminder hide")
    require(panel, "Responsive Tabelle", "status strip marker")
    require(panel, "nur Drei-Punkte-Menü öffnet Aktionen", "row action boundary marker")

    forbidden = [
        "tuev-card",
        "confirm_passed",
        "set_due_date",
    ]
    for needle in forbidden:
        if needle in panel:
            fail(f"Reminder Sidebar panel must not contain Card/action coupling {needle!r}")

    print("r053 sidebar responsive table width check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
