#!/usr/bin/env python3
"""Validate r056 Sidebar row-action identity hardening."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"
DOC = ROOT / "docs" / "REMINDER_R056_ROW_ACTION_IDENTITY_HARDENING.md"


def fail(message: str) -> None:
    raise SystemExit(f"r056 row action identity check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r081":
    fail("manifest version must be 0.1.0-r081")
if VERSION.read_text(encoding="utf-8").strip() != "r081":
    fail("REMINDER_VERSION.txt must be r056")

panel = PANEL.read_text(encoding="utf-8")
for needle, label in [
    ("this._openMenuEntryId = null;", "entry-id menu state"),
    ("_vehicleByEntryId(entryId)", "vehicle lookup helper"),
    ("data-menu-entry-id=", "menu entry id marker"),
    ("data-action-entry-id=", "action entry id marker"),
    ("this._openMenuEntryId === vehicle.entry_id", "entry id open-state comparison"),
    ("this._vehicleByEntryId(button.dataset.actionEntryId)", "entry id action resolution"),
    ("this._openMenuIndex = null", "legacy index state still cleared"),
    ("button[data-menu-index]", "legacy menu-index marker retained"),
]:
    require(panel, needle, label)

if panel.count("this._openMenuEntryId = null;") < 6:
    fail("open menu entry id should be cleared across create/edit/delete/filter/sort/close paths")

for forbidden in ["tuev-card", "confirm_passed", "set_due_date", "row.addEventListener(\"click\""]:
    if forbidden in panel:
        fail(f"forbidden coupling or full-row click remains: {forbidden}")

doc = DOC.read_text(encoding="utf-8")
require(doc, "entry_id", "r056 docs must explain entry id action identity")
require(doc, "No Card code", "r056 docs must preserve Reminder/Card separation")

print("r056 row action identity checks passed")
