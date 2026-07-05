#!/usr/bin/env python3
"""Validate r081 Sidebar list controls bundle."""
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
doc = read("docs/REMINDER_R078_SIDEBAR_SEARCH_BADGE_CONTROLS.md")
compat = read("docs/COMPAT_CARD_B355_REMINDER_R078.md")

require(manifest["version"] == "0.1.0-r089", "manifest version must be r083")
require(version == "r089", "REMINDER_VERSION must be r085")

for marker in [
    "_statusChip(label, value, count)",
    "_summaryChips(counts, visibleCount)",
    "data-status-chip",
    "status-filter-chip",
    "aria-pressed",
    "summary-chip-row",
    "summary-detail",
    "position: sticky",
    "status-pill::before",
    ]:
    require(marker in frontend, f"missing r081 list-control marker: {marker}")

for preserved in [
    "data-action-sheet-action=\"edit\"",
    "data-action-sheet-action=\"delete\"",
    "data-row-action=\"edit\"",
    "data-row-action=\"delete\"",
    "tuev_reminder/manager/vehicles/create",
    "tuev_reminder/manager/vehicles/update",
    "tuev_reminder/manager/vehicles/delete",
    "this._openRowMenu(Number(button.dataset.menuIndex))",
]:
    require(preserved in frontend or preserved in read("custom_components/tuev_reminder/manager_api.py"), f"missing preserved behavior marker: {preserved}")

for forbidden in [
    "import \"tuev-card",
    "from \"tuev-card",
    "custom:tuev-card",
]:
    require(forbidden not in frontend, f"Reminder frontend must not import/use Card code: {forbidden}")

require("Reminder r081" in readme, "README must describe r081")
require("Sidebar Search Badge Controls" in handover, "HANDOVER must describe r081")
require("Sidebar Search Badge Controls" in changelog, "CHANGELOG must retain Sidebar Search Badge Controls entry")
require("No release candidate" in doc or "No release-candidate" in doc, "r081 doc must explicitly avoid release scope")
require("Card remains a separate" in compat, "compat doc must preserve Card separation")

print("r081 Sidebar list controls bundle checks passed")
