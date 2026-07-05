#!/usr/bin/env python3
"""Validate r055 mobile action-sheet tap-race hardening."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"


def fail(message: str) -> None:
    raise SystemExit(f"r055 mobile action-sheet tap-race check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r087":
    fail("manifest version must be 0.1.0-r087")
if VERSION.read_text(encoding="utf-8").strip() != "r087":
    fail("REMINDER_VERSION.txt must be r055")

panel = PANEL.read_text(encoding="utf-8")
require(panel, "this._actionSheetCloseGuardUntil = 0;", "action-sheet close guard state")
require(panel, "this._actionSheetCloseGuardUntil = this._actionSheetOpenedAt + 650;", "open-tap close guard window")
require(panel, "_closeActionSheet({ force = false } = {})", "guarded action-sheet close helper")
require(panel, "Date.now() < this._actionSheetCloseGuardUntil", "close guard condition")
require(panel, "button.addEventListener(\"click\", openMenu);", "single click based row action open")
require(panel, "actionSheetBackdrop.addEventListener(\"pointerup\", maybeCloseActionSheet);", "backdrop pointerup guard")
require(panel, "actionSheetBackdrop.addEventListener(\"click\", maybeCloseActionSheet);", "backdrop click guard")
require(panel, "this._closeActionSheet({ force: true })", "explicit forced close for user close actions")
require(panel, "z-index: 2147483000;", "action-sheet z-index above HA content")

for forbidden in [
    'button.addEventListener("pointerup", (event) => {\n        handledPointer = true;',
    "HU bestanden",
    "tuev-card",
    "hui-card",
]:
    if forbidden in panel:
        fail(f"forbidden coupling or old tap-race pattern remains: {forbidden}")

print("r055 mobile action-sheet tap-race checks passed")
