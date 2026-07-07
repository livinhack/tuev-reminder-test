#!/usr/bin/env python3
"""Validate r081 sidebar search clear button and badge-row reset cleanup."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"


def fail(message: str) -> None:
    raise SystemExit(message)

manifest = json.loads((ROOT / "custom_components" / "tuev_reminder" / "manifest.json").read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r114":
    fail("manifest version must be 0.1.0-r114")
if (ROOT / "REMINDER_VERSION.txt").read_text(encoding="utf-8").strip() != "r114":
    fail("REMINDER_VERSION must be r085")

panel = PANEL.read_text(encoding="utf-8")
required = [
    'class="search-clear"',
    'id="clear-search"',
    'title="Suche leeren"',
    'aria-label="Suche leeren"',
    '.search-clear[hidden] { display: none; }',
    'class="status-filter-chip',
]
for needle in required:
    if needle not in panel:
        fail(f"missing r081 search clear marker: {needle}")

for forbidden in [
    'class="filter-reset-chip"',
    'data-reset-filters',
    '[data-reset-filters]',
    '.filter-reset-chip',
    'id="status-filter"',
    'id="refresh"',
    '>Aktualisieren<',
    'querySelector("#refresh")',
    'querySelector("#status-filter")',
]:
    if forbidden in panel:
        fail(f"obsolete toolbar/reset control present: {forbidden}")

print("r081 sidebar search clear button check passed")
