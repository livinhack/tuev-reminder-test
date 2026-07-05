#!/usr/bin/env python3
"""Validate r081 sidebar search/badge control cleanup."""
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
    'id="filter"',
    'data-status-chip',
    '_statusChip("Alle", "all", total)',
    '_statusChip("Abgelaufen", "expired", counts.expired || 0)',
    '_statusChip("Fällig", "due", counts.due || 0)',
    '_statusChip("Gültig", "valid", counts.valid || 0)',
]
for needle in required:
    if needle not in panel:
        fail(f"missing r081 sidebar control marker: {needle}")

for forbidden in [
    'id="status-filter"',
    'aria-label="Statusfilter"',
    'id="refresh"',
    '>Aktualisieren<',
    'Lädt …" : "Aktualisieren',
    'querySelector("#refresh")',
    'querySelector("#status-filter")',
]:
    if forbidden in panel:
        fail(f"obsolete toolbar control still present: {forbidden}")

if 'grid-template-columns: minmax(240px, 1fr);' not in panel:
    fail("toolbar must be a single search-column grid in r081")

print("r081 sidebar search/badge controls check passed")
