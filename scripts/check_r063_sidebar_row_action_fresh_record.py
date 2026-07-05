#!/usr/bin/env python3
"""Validate r063 Sidebar row-action fresh record hardening."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
DOC = ROOT / "docs" / "REMINDER_R063_SIDEBAR_ROW_ACTION_FRESH_RECORD.md"
COMPAT = ROOT / "docs" / "COMPAT_CARD_B355_REMINDER_R063.md"
README = ROOT / "README.md"
HANDOVER = ROOT / "HANDOVER.md"


def fail(message: str) -> None:
    raise SystemExit(f"r063 sidebar row action fresh record check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r089":
    fail("manifest version must be 0.1.0-r089")
if VERSION.read_text(encoding="utf-8").strip() != "r089":
    fail("REMINDER_VERSION.txt must be r063")

panel = PANEL.read_text(encoding="utf-8")
for needle, label in [
    ("_rowActionLoadingEntryId", "row action loading guard"),
    ("async _fetchVehicleRecord(vehicle)", "fresh vehicle fetch helper"),
    ('type: "tuev_reminder/manager/vehicles/get"', "vehicles/get call"),
    ("entry_id: entryId", "entry id fetch payload"),
    ("this._vehicles = this._vehicles.map", "local cache replacement"),
    ("async _handleRowAction(action, vehicle)", "async row action handler"),
    ("Fahrzeugdaten konnten nicht geladen werden. Die Liste wurde aktualisiert.", "stale entry error flash"),
    ("aria-busy", "busy action button marker"),
    ("frische Edit/Delete-Daten", "summary strip row-action label"),
]:
    require(panel, needle, label)

# r063 must not add Card coupling.
for forbidden in [
    "tuev-card.js",
    "custom:tuev-card",
    "confirm_passed",
]:
    if forbidden in panel:
        fail(f"unexpected Card/action coupling in panel: {forbidden}")

require(DOC.read_text(encoding="utf-8"), "vehicles/get", "r063 doc vehicles/get note")
require(COMPAT.read_text(encoding="utf-8"), "No Card renderer", "compat Card separation")
require(README.read_text(encoding="utf-8"), "r063 highlights", "README r063 section")
require(HANDOVER.read_text(encoding="utf-8"), "Sidebar Row Action Fresh Record", "handover r063 title")

print("r063 sidebar row action fresh record checks passed")
