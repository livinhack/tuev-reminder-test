#!/usr/bin/env python3
"""Validate r081 Sidebar UX structure bundle."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
version = read("REMINDER_VERSION.txt").strip()
frontend = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")
readme = read("README.md")
handover = read("HANDOVER.md")
changelog = read("CHANGELOG.md")
doc = read("docs/REMINDER_R076_SIDEBAR_UX_STRUCTURE_BUNDLE.md")
compat = read("docs/COMPAT_CARD_B355_REMINDER_R076.md")

require(manifest["version"] == "0.1.0-r100", "manifest version must be r083")
require(version == "r100", "REMINDER_VERSION must be r085")

for marker in [
    "form-stack fields-stack",
    "section-kicker",
    "HU & Erinnerung",
    "Art & Nummer",
    "Saisonzeitraum",
    "summary-list",
    "Die Sidebar verwaltet nur Reminder-Daten",
    "color-mix(in srgb, var(--error-color)",
]:
    require(marker in frontend, f"missing r081 UI marker: {marker}")

for preserved in [
    "tuev_reminder/manager/vehicles/create",
    "tuev_reminder/manager/vehicles/update",
    "tuev_reminder/manager/vehicles/delete",
    "data-action-sheet-action=\"edit\"",
    "Ungespeicherte Änderungen",
    "Duplicate",
]:
    require(preserved in frontend or preserved in read("custom_components/tuev_reminder/manager_api.py"), f"missing preserved marker: {preserved}")

for forbidden in [
    "import \"tuev-card",
    "from \"tuev-card",
    "custom:tuev-card",
]:
    require(forbidden not in frontend, f"Reminder frontend must not import/use Card code: {forbidden}")

require("Reminder r081" in readme, "README must describe r081")
require("Sidebar UX Structure Bundle" in handover, "HANDOVER must describe r081")
require("Sidebar UX Structure Bundle" in changelog, "CHANGELOG must retain Sidebar UX Structure Bundle entry")
require("No release flow" in doc, "r081 doc must explicitly avoid release scope")
require("Card remains a separate" in compat, "compat doc must preserve Card separation")

print("r081 Sidebar UX structure bundle checks passed")
