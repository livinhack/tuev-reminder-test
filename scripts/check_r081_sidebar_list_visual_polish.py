#!/usr/bin/env python3
"""Validate r081 sidebar list visual polish and mobile card layout."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"


def fail(message: str) -> None:
    raise SystemExit(message)

manifest = json.loads((ROOT / "custom_components" / "tuev_reminder" / "manifest.json").read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r081":
    fail("manifest version must be 0.1.0-r081")
if (ROOT / "REMINDER_VERSION.txt").read_text(encoding="utf-8").strip() != "r081":
    fail("REMINDER_VERSION must be r081")

panel = PANEL.read_text(encoding="utf-8")
required = [
    'class="vehicle-row row-status-${this._escape(this._statusClass(vehicle.status))}"',
    'class="vehicle-meta-line">${this._vehicleMeta(vehicle)}</div>',
    'class="main-value hu-value status-text-${this._escape(this._statusClass(vehicle.status))}"',
    '.vehicle-row.row-status-expired',
    '.vehicle-row.row-status-due',
    '.vehicle-row.row-status-valid',
    '.vehicle-meta-line { display: flex;',
    '.status-text-expired { color: var(--error-color); }',
    '@media (max-width: 720px) {',
    '.manager-table thead { display: none; }',
    '.vehicle-row {',
    'grid-template-columns: 96px minmax(0, 1fr);',
    'mobile Kartenansicht',
]
for needle in required:
    if needle not in panel:
        fail(f"missing r081 list polish marker: {needle}")

for forbidden in [
    'id="status-filter"',
    'id="refresh"',
    '>Aktualisieren<',
    'class="filter-reset-chip"',
]:
    if forbidden in panel:
        fail(f"obsolete control present in r081: {forbidden}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
handover = (ROOT / "HANDOVER.md").read_text(encoding="utf-8")
changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
for needle in [
    "Reminder r081",
    "mobile card layout",
    "No release packaging",
]:
    if needle not in readme:
        fail(f"README missing r081 note: {needle}")
if "Sidebar List Visual Polish / Mobile Card Layout" not in handover:
    fail("HANDOVER must describe r081 visual polish")
if "r081 – Sidebar List Visual Polish / Mobile Card Layout" not in changelog:
    fail("CHANGELOG must contain r081 entry")
if not (ROOT / "docs" / "REMINDER_R081_SIDEBAR_LIST_VISUAL_POLISH.md").exists():
    fail("r081 documentation file missing")
if not (ROOT / "docs" / "COMPAT_CARD_B355_REMINDER_R081.md").exists():
    fail("r081 compatibility file missing")

print("r081 sidebar list visual polish checks passed")
