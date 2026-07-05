#!/usr/bin/env python3
"""Validate r062 Sidebar duplicate preflight validation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
DOC = ROOT / "docs" / "REMINDER_R062_SIDEBAR_DUPLICATE_PREFLIGHT.md"
COMPAT = ROOT / "docs" / "COMPAT_CARD_B355_REMINDER_R062.md"
README = ROOT / "README.md"
HANDOVER = ROOT / "HANDOVER.md"


def fail(message: str) -> None:
    raise SystemExit(f"r062 sidebar duplicate preflight check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r081":
    fail("manifest version must be 0.1.0-r081")
if VERSION.read_text(encoding="utf-8").strip() != "r081":
    fail("REMINDER_VERSION.txt must be r062")

panel = PANEL.read_text(encoding="utf-8")
for needle, label in [
    ("_duplicateKey(value)", "duplicate key helper"),
    ("_formDuplicateErrors()", "duplicate preflight helper"),
    ("const currentEntryId = this._view === \"detail\" ? String(this._selectedVehicle?.entry_id || \"\") : \"\";", "edit mode entry exclusion"),
    ("vehicle.entry_id", "vehicle entry id duplicate exclusion"),
    ("Ein Fahrzeug mit diesem Namen existiert bereits.", "duplicate name message"),
    ("Ein Fahrzeug mit diesem Kennzeichen existiert bereits.", "duplicate plate message"),
    ("this._formDuplicateErrors().forEach((error) => errors.push(error));", "validation integration"),
    ("Duplicate-Schutz · lokale Duplicate-Prüfung", "summary strip label"),
]:
    require(panel, needle, label)

# Backend duplicate guard must still exist; r062 is UI preflight, not a backend rollback.
api = (ROOT / "custom_components" / "tuev_reminder" / "manager_api.py").read_text(encoding="utf-8")
require(api, "_duplicate_vehicle_errors", "backend duplicate guard")
require(api, "current_entry_id", "backend update exclusion")

doc = DOC.read_text(encoding="utf-8")
require(doc, "backend duplicate guard remains authoritative", "r062 doc backend authority note")
compat = COMPAT.read_text(encoding="utf-8")
require(compat, "No Card renderer", "compat Card separation")
require(README.read_text(encoding="utf-8"), "r062 highlights", "README r062 section")
require(HANDOVER.read_text(encoding="utf-8"), "Sidebar Duplicate Preflight", "handover r062 title")

print("r062 sidebar duplicate preflight checks passed")
