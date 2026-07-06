#!/usr/bin/env python3
"""Validate r065 Sidebar dialog keyboard/focus hardening."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
DOC = ROOT / "docs" / "REMINDER_R065_SIDEBAR_DIALOG_KEYBOARD_FOCUS.md"
COMPAT = ROOT / "docs" / "COMPAT_CARD_B355_REMINDER_R065.md"
README = ROOT / "README.md"
HANDOVER = ROOT / "HANDOVER.md"


def fail(message: str) -> None:
    raise SystemExit(f"r065 sidebar dialog keyboard/focus check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r108":
    fail("manifest version must be 0.1.0-r108")
if VERSION.read_text(encoding="utf-8").strip() != "r108":
    fail("REMINDER_VERSION.txt must be r071")

panel = PANEL.read_text(encoding="utf-8")

for needle, label in [
    ("_dialogFocusPending", "dialog focus pending state"),
    ('role="dialog" aria-modal="true" tabindex="-1"', "focusable modal/dialog backdrops"),
    ('page.addEventListener("keydown"', "central page Escape handler"),
    ('event.key !== "Escape"', "Escape key guard"),
    ('this._closeActionSheet({ force: true })', "Escape action sheet close"),
    ('this._closeRowMenu()', "Escape row menu close"),
    ('this._closeForm()', "Escape guarded form close"),
    ('this._dialogFocusPending = "discard"', "discard focus request"),
    ('this._dialogFocusPending = "actionSheet"', "action sheet focus request"),
    ('this._dialogFocusPending = "modal"', "modal focus request"),
    ('focus({ preventScroll: true })', "prevent-scroll focus"),
    ('event.stopPropagation();', "Escape propagation guard"),
]:
    require(panel, needle, label)

if "window.confirm" in panel:
    fail("native window.confirm dirty guard must not be used")

for forbidden in [
    "tuev-card.js",
    "custom:tuev-card",
    "confirm_passed",
]:
    if forbidden in panel:
        fail(f"unexpected Card/action coupling in panel: {forbidden}")

require(DOC.read_text(encoding="utf-8"), "Escape handling", "r065 doc Escape note")
require(COMPAT.read_text(encoding="utf-8"), "Card remains", "compat Card separation")
require(README.read_text(encoding="utf-8"), "r065 highlights", "README r065 section")
require(HANDOVER.read_text(encoding="utf-8"), "Sidebar Dialog Keyboard Focus", "handover r065 title")

print("r065 sidebar dialog keyboard/focus checks passed")
