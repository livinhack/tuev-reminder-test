#!/usr/bin/env python3
"""Validate r083 Sidebar meta line removal."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"


def fail(message: str) -> None:
    raise SystemExit(message)

manifest = json.loads((ROOT / "custom_components" / "tuev_reminder" / "manifest.json").read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r100":
    fail("manifest version must be 0.1.0-r100")
if (ROOT / "REMINDER_VERSION.txt").read_text(encoding="utf-8").strip() != "r100":
    fail("REMINDER_VERSION must be r085")

panel = PANEL.read_text(encoding="utf-8")
required = [
    'class="main-value hu-value">${this._escape(this._monthYear(vehicle))}</div>',
    'class="status-pill status-${this._escape(this._statusClass(vehicle.status))}">${this._escape(this._statusLabel(vehicle.status))}</span>',
    'class="preview-cell" data-label="Kennzeichen">',
    '${this._platePreview(vehicle)}',
    'class="vehicle-row',
]
for needle in required:
    if needle not in panel:
        fail(f"missing r083 list marker: {needle}")

for forbidden in [
    '_vehicleMeta(vehicle)',
    'vehicle-meta-line',
    'class="tag"',
    '.tag-row',
    '.tag {',
    'tags.push("H")',
    'tags.push("E")',
    'tags.push("Grün")',
    'tags.push(`Saison ${vehicle.season_start_month}–${vehicle.season_end_month}`);',
    'tags.push("Wechsel")',
    'class="vehicle-row row-status-${this._escape(this._statusClass(vehicle.status))}"',
    'status-text-${this._escape(this._statusClass(vehicle.status))}',
    '.status-text-expired',
    '.status-text-due',
    '.status-text-valid',
    '.vehicle-row.row-status-expired',
    '.vehicle-row.row-status-due',
    '.vehicle-row.row-status-valid',
]:
    if forbidden in panel:
        fail(f"r083 obsolete list/meta marker still present: {forbidden}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
handover = (ROOT / "HANDOVER.md").read_text(encoding="utf-8")
changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
for needle in ["Reminder r083", "meta/tag line", "Card-aware"]:
    if needle not in readme:
        fail(f"README missing r083 note: {needle}")
if "Sidebar Meta Line Removal" not in handover:
    fail("HANDOVER must describe r083 meta line removal")
if "r083 – Sidebar Meta Line Removal" not in changelog:
    fail("CHANGELOG must contain r083 entry")
if not (ROOT / "docs" / "REMINDER_R083_SIDEBAR_META_LINE_REMOVAL.md").exists():
    fail("r083 documentation file missing")
if not (ROOT / "docs" / "COMPAT_CARD_B355_REMINDER_R083.md").exists():
    fail("r083 compatibility file missing")

print("r083 Sidebar meta line removal checks passed")
