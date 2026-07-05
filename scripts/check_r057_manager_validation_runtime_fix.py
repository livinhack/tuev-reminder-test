#!/usr/bin/env python3
"""Validate r057 Manager validation runtime fix."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"
API = ROOT / "custom_components" / "tuev_reminder" / "manager_api.py"
DOC = ROOT / "docs" / "REMINDER_R057_MANAGER_VALIDATION_RUNTIME_FIX.md"
COMPAT = ROOT / "docs" / "COMPAT_CARD_B355_REMINDER_R057.md"


def fail(message: str) -> None:
    raise SystemExit(f"r057 manager validation runtime check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r077":
    fail("manifest version must be 0.1.0-r077")
if VERSION.read_text(encoding="utf-8").strip() != "r077":
    fail("REMINDER_VERSION.txt must be r057")

api = API.read_text(encoding="utf-8")
for needle, label in [
    ("_FIELD_ERROR_MESSAGES", "friendly field error map"),
    ("def _validation_error_message(field_errors: dict, duplicate_errors: list[str])", "validation message helper"),
    ("field_errors, normalized = validate_and_normalize_vehicle_payload", "separate field errors"),
    ("duplicate_errors = _duplicate_vehicle_errors", "separate duplicate errors"),
    ("if field_errors or duplicate_errors:", "combined validation branch"),
    ("_validation_error_message(field_errors, duplicate_errors)", "friendly validation send_error message"),
    ("Ein Fahrzeug mit diesem Namen existiert bereits.", "duplicate name message"),
    ("Ein Fahrzeug mit diesem Kennzeichen existiert bereits.", "duplicate plate message"),
]:
    require(api, needle, label)

for forbidden in [
    "errors.extend(_duplicate_vehicle_errors",
    "f\"TÜV Reminder vehicle data is invalid: {errors}\"",
]:
    if forbidden in api:
        fail(f"old broken validation path still present: {forbidden}")

if api.count("field_errors, normalized = validate_and_normalize_vehicle_payload") != 2:
    fail("create and update should both use separate field_errors variables")
if api.count("duplicate_errors = _duplicate_vehicle_errors") != 2:
    fail("create and update should both use separate duplicate_errors variables")

doc = DOC.read_text(encoding="utf-8")
require(doc, ".extend(...)", "r057 docs must explain the runtime bug")
require(doc, "No Card code", "r057 docs must preserve Reminder/Card separation")
compat = COMPAT.read_text(encoding="utf-8")
require(compat, "Card bridge fields", "compat note must mention unchanged Card bridge")
require(compat, "separate project", "compat note must preserve repo separation")

print("r057 manager validation runtime checks passed")
