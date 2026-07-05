#!/usr/bin/env python3
"""Validate r053 Sidebar CRUD hardening and feedback."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")

def fail(message: str) -> None:
    raise SystemExit(f"r053 sidebar CRUD hardening check failed: {message}")

manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
if manifest.get("version") != "0.1.0-r097":
    fail("manifest version must be 0.1.0-r097")
if read("REMINDER_VERSION.txt").strip() != "r097":
    fail("REMINDER_VERSION.txt must be r053")

api = read("custom_components/tuev_reminder/manager_api.py")
panel = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")

def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle}")

require(api, "def _duplicate_vehicle_errors", "backend duplicate guard helper")
require(api, "merged_entry_values", "existing-entry comparison")
require(api, "plate_parts_from_values(normalized)", "normalized plate comparison")
require(api, "Ein Fahrzeug mit diesem Namen existiert bereits.", "duplicate name error")
require(api, "Ein Fahrzeug mit diesem Kennzeichen existiert bereits.", "duplicate plate error")
require(api, "current_entry_id=entry.entry_id", "update self-exclusion")

require(panel, "_setFlash(message", "frontend flash helper")
require(panel, "Fahrzeug wurde angelegt.", "create success feedback")
require(panel, "Änderungen wurden gespeichert.", "update success feedback")
require(panel, "Fahrzeug wurde gelöscht.", "delete success feedback")
require(panel, "class=\"flash", "flash render")
require(panel, "Duplicate-Schutz", "summary hardening marker")

print("r053 sidebar CRUD hardening check OK")
