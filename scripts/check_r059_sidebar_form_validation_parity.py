#!/usr/bin/env python3
"""Validate r060 Sidebar form validation parity."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
DOC = ROOT / "docs" / "REMINDER_R060_SIDEBAR_FORM_VALIDATION_PARITY.md"
COMPAT = ROOT / "docs" / "COMPAT_CARD_B355_REMINDER_R060.md"


def fail(message: str) -> None:
    raise SystemExit(f"r060 sidebar form validation parity check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r081":
    fail("manifest version must be 0.1.0-r081")
if VERSION.read_text(encoding="utf-8").strip() != "r081":
    fail("REMINDER_VERSION.txt must be r060")

panel = PANEL.read_text(encoding="utf-8")
for needle, label in [
    ("_renderIntervalOptions(selected)", "interval select helper"),
    ('<label>Intervall<select data-field="interval">', "interval select field"),
    ("Prüfintervall muss 1 oder 2 Jahre betragen.", "local interval validation"),
    ("HU-Jahr muss zwischen 1900 und 2100 liegen.", "backend-aligned year validation"),
    ('type="number" inputmode="numeric" min="1900" max="2100" step="1"', "HU year input constraints"),
    ("Erinnerungs-Vorlauf Tage", "German reminder offset label"),
    ('type="number" inputmode="numeric" min="0" max="365" step="1"', "reminder offset input constraints"),
    ('maxlength="1" pattern="[0-9]"', "change-plate digit constraint"),
    ("lokale Formularvalidierung auf Backend-Regeln abgestimmt", "summary strip r060 marker"),
]:
    require(panel, needle, label)

if "<label>Intervall<input" in panel:
    fail("interval must no longer be a free numeric input")
if "HU-Jahr muss zwischen 2000 und 2100 liegen." in panel:
    fail("old local year range still present")

require(DOC.read_text(encoding="utf-8"), "source of truth", "backend source-of-truth documentation")
compat = COMPAT.read_text(encoding="utf-8")
require(compat, "Card bridge fields", "compat note must mention unchanged Card bridge")
require(compat, "separate project", "compat note must preserve repo separation")

print("r060 sidebar form validation parity checks passed")
