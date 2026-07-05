#!/usr/bin/env python3
"""Validate r066 Sidebar form payload scrubbing."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
DOC = ROOT / "docs" / "REMINDER_R066_SIDEBAR_FORM_PAYLOAD_SCRUB.md"
COMPAT = ROOT / "docs" / "COMPAT_CARD_B355_REMINDER_R066.md"
README = ROOT / "README.md"
HANDOVER = ROOT / "HANDOVER.md"


def fail(message: str) -> None:
    raise SystemExit(f"r066 sidebar form payload scrub check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r066":
    fail("manifest version must be 0.1.0-r066")
if VERSION.read_text(encoding="utf-8").strip() != "r066":
    fail("REMINDER_VERSION.txt must be r066")

panel = PANEL.read_text(encoding="utf-8")

for needle, label in [
    ("_formKindFlags", "central form kind flags helper"),
    ("_scrubFormForKind", "form scrub helper"),
    ("_sanitizeFieldValue", "field sanitizer"),
    ('clean.plate = "";', "change mode normal plate scrub"),
    ('clean.change_plate_common_text = "";', "non-change common text scrub"),
    ('clean.change_plate_vehicle_digit = "";', "non-change vehicle digit scrub"),
    ('clean.plate_suffix_h = false;', "suffix H scrub"),
    ('clean.plate_suffix_e = false;', "suffix E scrub"),
    ('season_start_month: ["seasonal", "green_seasonal"].includes(clean.plate_kind) ? Number(clean.season_start_month || 4) : null', "non-seasonal start month neutral payload"),
    ('season_end_month: ["seasonal", "green_seasonal"].includes(clean.plate_kind) ? Number(clean.season_end_month || 10) : null', "non-seasonal end month neutral payload"),
    ('this._form = this._scrubFormForKind({', "set form value uses scrubbed state"),
    ('this._form = this._scrubFormForKind({\n      ...this._defaultForm(),', "detail form opens scrubbed"),
    ('const clean = this._scrubFormForKind();', "scrubbed state used in validation/render"),
]:
    require(panel, needle, label)

for forbidden in [
    "tuev-card.js",
    "custom:tuev-card",
    "confirm_passed",
]:
    if forbidden in panel:
        fail(f"unexpected Card/action coupling in panel: {forbidden}")

require(DOC.read_text(encoding="utf-8"), "hidden or inactive fields", "r066 doc payload scrub note")
require(COMPAT.read_text(encoding="utf-8"), "Card remains", "compat Card separation")
require(README.read_text(encoding="utf-8"), "r066 highlights", "README r066 section")
require(HANDOVER.read_text(encoding="utf-8"), "Sidebar Form Payload Scrub", "handover r066 title")

print("r066 sidebar form payload scrub checks passed")
