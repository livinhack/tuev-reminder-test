#!/usr/bin/env python3
"""Validate r061 backend reminder-offset validation parity."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"
MANAGER = ROOT / "custom_components" / "tuev_reminder" / "manager.py"
API = ROOT / "custom_components" / "tuev_reminder" / "manager_api.py"
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
DOC = ROOT / "docs" / "REMINDER_R061_BACKEND_OFFSET_VALIDATION.md"
COMPAT = ROOT / "docs" / "COMPAT_CARD_B355_REMINDER_R061.md"


def fail(message: str) -> None:
    raise SystemExit(f"r061 backend offset validation check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r078":
    fail("manifest version must be 0.1.0-r078")
if VERSION.read_text(encoding="utf-8").strip() != "r078":
    fail("REMINDER_VERSION.txt must be r062")

manager = MANAGER.read_text(encoding="utf-8")
api = API.read_text(encoding="utf-8")
panel = PANEL.read_text(encoding="utf-8")

for needle, label in [
    ("reminder_offset_days = _int_or_default(payload.get(CONF_REMINDER_OFFSET_DAYS), DEFAULT_REMINDER_OFFSET_DAYS)", "write-path offset parse"),
    ("if not 0 <= reminder_offset_days <= 365:", "offset range guard"),
    ("errors[CONF_REMINDER_OFFSET_DAYS] = \"invalid_offset\"", "offset validation error"),
    ("reminder_offset_days = min(365, max(0, reminder_offset_days))", "bounded normalized fallback"),
]:
    require(manager, needle, label)

if "reminder_offset_days = reminder_offset_days_from_values(payload)" in manager:
    fail("write validation still reuses read-side clamping helper for payload validation")

for needle, label in [
    ("CONF_REMINDER_OFFSET_DAYS", "offset constant import/use"),
    ("(CONF_REMINDER_OFFSET_DAYS, \"invalid_offset\")", "friendly offset error mapping"),
    ("Erinnerungs-Vorlauf muss zwischen 0 und 365 Tagen liegen.", "German offset error message"),
]:
    require(api, needle, label)

require(panel, "<h3>Kennzeichen</h3>", "modal Kennzeichen heading")
if "<h3>Vorschau</h3>" in panel:
    fail("old modal heading Vorschau still present")

require(DOC.read_text(encoding="utf-8"), "silently clamping", "r061 docs must explain old direct-payload behavior")
compat = COMPAT.read_text(encoding="utf-8")
require(compat, "Card-facing attributes", "compat note must mention unchanged Card-facing contract")
require(compat, "separate project", "compat note must preserve Reminder/Card separation")

print("r061 backend offset validation checks passed")
