#!/usr/bin/env python3
"""Validate r064 Sidebar unsaved-changes dialog."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
DOC = ROOT / "docs" / "REMINDER_R064_SIDEBAR_UNSAVED_CHANGES_DIALOG.md"
COMPAT = ROOT / "docs" / "COMPAT_CARD_B355_REMINDER_R064.md"
README = ROOT / "README.md"
HANDOVER = ROOT / "HANDOVER.md"


def fail(message: str) -> None:
    raise SystemExit(f"r064 sidebar unsaved changes dialog check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r108":
    fail("manifest version must be 0.1.0-r108")
if VERSION.read_text(encoding="utf-8").strip() != "r108":
    fail("REMINDER_VERSION.txt must be r064")

panel = PANEL.read_text(encoding="utf-8")
if "window.confirm" in panel:
    fail("native window.confirm dirty guard must not be used in r064")

for needle, label in [
    ("_discardPromptOpen", "discard prompt state"),
    ("_shouldPromptDiscardChanges()", "discard prompt predicate"),
    ("_openDiscardPrompt()", "discard prompt opener"),
    ("_closeDiscardPrompt()", "discard prompt closer"),
    ("_renderDiscardConfirm()", "discard dialog renderer"),
    ("Ungespeicherte Änderungen", "discard dialog title"),
    ("id=\"confirm-discard\"", "discard confirm button"),
    ("id=\"cancel-discard\"", "discard cancel button"),
    ("this._openDiscardPrompt()", "close form prompt path"),
    ("this._closeForm({ force: true })", "force close discard action"),
    (".discard-backdrop", "discard backdrop styling/handler"),
]:
    require(panel, needle, label)

for forbidden in [
    "tuev-card.js",
    "custom:tuev-card",
    "confirm_passed",
]:
    if forbidden in panel:
        fail(f"unexpected Card/action coupling in panel: {forbidden}")

require(DOC.read_text(encoding="utf-8"), "window.confirm", "r064 doc native confirm note")
require(COMPAT.read_text(encoding="utf-8"), "Card remains", "compat Card separation")
require(README.read_text(encoding="utf-8"), "r064 highlights", "README r064 section")
require(HANDOVER.read_text(encoding="utf-8"), "Sidebar Unsaved Changes Dialog", "handover r064 title")

print("r064 sidebar unsaved changes dialog checks passed")
