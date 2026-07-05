#!/usr/bin/env python3
"""Validate r053 Sidebar dirty guard and unchanged edit save behavior."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"


def fail(message: str) -> None:
    raise SystemExit(f"r053 sidebar dirty guard check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("version") != "0.1.0-r060":
        fail("manifest version must be 0.1.0-r060")
    if VERSION.read_text(encoding="utf-8").strip() != "r060":
        fail("REMINDER_VERSION.txt must be r053")

    panel = PANEL.read_text(encoding="utf-8")
    require(panel, "this._formSnapshot = null", "form snapshot state")
    require(panel, "_payloadKey(payload = this._formPayload())", "normalized payload snapshot helper")
    require(panel, "_rememberFormSnapshot()", "snapshot capture helper")
    require(panel, "_formDirty()", "dirty-state helper")
    require(panel, "_confirmDiscardChanges()", "discard confirmation helper")
    require(panel, "Ungespeicherte Änderungen verwerfen?", "discard confirmation text")
    require(panel, "this._view === \"detail\" && !this._formDirty()", "unchanged edit validation branch")
    require(panel, "Keine Änderungen", "unchanged edit summary")
    require(panel, "!this._formDirty() ? \"disabled\"", "edit save disabled until dirty")
    require(panel, "Dirty-Guard", "status strip marker")

    forbidden = [
        "tuev-card",
        "confirm_passed",
        "set_due_date",
    ]
    for needle in forbidden:
        if needle in panel:
            fail(f"Reminder Sidebar panel must not contain Card/action coupling {needle!r}")

    print("r053 sidebar dirty guard check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
