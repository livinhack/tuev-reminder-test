#!/usr/bin/env python3
"""Validate r060 Sidebar plate-format-by-kind UI parity."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
DOC = ROOT / "docs" / "REMINDER_R060_PLATE_FORMAT_BY_KIND_UI.md"
COMPAT = ROOT / "docs" / "COMPAT_CARD_B355_REMINDER_R060.md"


def fail(message: str) -> None:
    raise SystemExit(f"r060 plate format by kind UI check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r097":
    fail("manifest version must be 0.1.0-r097")
if VERSION.read_text(encoding="utf-8").strip() != "r097":
    fail("REMINDER_VERSION.txt must be r060")

panel = PANEL.read_text(encoding="utf-8")
for needle, label in [
    ("_allowedPlateFormatValues(kind = this._form.plate_kind)", "allowed-format helper"),
    ("this._metadata?.plate_formats_by_kind", "metadata-driven format map"),
    ("_plateFormatOptionsForKind(kind = this._form.plate_kind)", "filtered format options helper"),
    ("const plateFormats = this._plateFormatOptionsForKind(clean.plate_kind);", "form uses filtered formats"),
    ("Kennzeichenformat passt nicht zur Kennzeichenart.", "local compatibility validation"),
    ("const allowedFormats = this._allowedPlateFormatValues(clean.plate_kind);", "kind-change allowed format recalculation"),
    ("clean.plate_format = allowedFormats[0] || \"single_line\";", "incompatible format reset"),
]:
    require(panel, needle, label)

if "const plateFormats = this._metadata?.plate_formats ||" in panel:
    fail("form still renders all plate formats without filtering")

require(DOC.read_text(encoding="utf-8"), "plate_formats_by_kind", "r060 documentation must mention metadata contract")
compat = COMPAT.read_text(encoding="utf-8")
require(compat, "unchanged from r059", "compat note must say Card-facing contract is unchanged")
require(compat, "separate project", "compat note must preserve Reminder/Card separation")

print("r060 plate format by kind UI checks passed")
