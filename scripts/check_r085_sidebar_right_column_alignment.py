#!/usr/bin/env python3
"""Validate r085 Sidebar right column alignment polish."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
manifest = json.loads((ROOT / "custom_components" / "tuev_reminder" / "manifest.json").read_text(encoding="utf-8"))
assert manifest.get("version") == "0.1.0-r100"
assert (ROOT / "REMINDER_VERSION.txt").read_text(encoding="utf-8").strip() == "r100"
panel = PANEL.read_text(encoding="utf-8")
for needle in [
    'table-layout: fixed;',
    'class="preview-cell" data-label="Kennzeichen"><div class="row-end-stack">',
    '.row-end-stack {',
    'justify-content: flex-end;',
    '.col-preview { width: 190px; text-align: right; }',
    '.menu-cell { position: relative; text-align: center;',
    'width: min(170px, 100%);',
    'max-width: 170px;',
    'min-width: 118px;',
    'height: 32px;',
]:
    if needle not in panel:
        raise AssertionError(f"missing r085 right-column marker: {needle}")
for forbidden in [
    'class="preview-cell" data-label="Kennzeichen">${this._platePreview(vehicle)}</td>',
    '.col-preview { width: 240px; text-align: right; }',
]:
    if forbidden in panel:
        raise AssertionError(f"obsolete r084 right-column marker still present: {forbidden}")
assert (ROOT / "docs" / "REMINDER_R085_SIDEBAR_RIGHT_COLUMN_ALIGNMENT.md").exists()
assert (ROOT / "docs" / "COMPAT_CARD_B355_REMINDER_R085.md").exists()
print("r085 sidebar right-column alignment checks passed")
