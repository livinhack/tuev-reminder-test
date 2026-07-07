#!/usr/bin/env python3
"""Validate r112 bundled dialog accessibility/save-state cleanup."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components/tuev_reminder/manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"
DOC = ROOT / "docs/REMINDER_R111_SIDEBAR_DIALOG_ACCESSIBILITY_CLEANUP.md"

panel = PANEL.read_text(encoding="utf-8")
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
version = VERSION.read_text(encoding="utf-8").strip()
doc = DOC.read_text(encoding="utf-8")

assert manifest["version"] == "0.1.0-r114"
assert version == "r114"
assert "Reminder r111" in doc or "Sidebar Dialog Accessibility Cleanup" in doc
assert "r114 is a bundled cleanup/checkpoint before the next feature block" in panel
assert "dialogs carry labelled/described modal semantics and busy state" in panel

for needle in [
    'aria-labelledby="vehicle-form-title" aria-describedby="vehicle-form-description" aria-busy="${this._saving ? "true" : "false"}"',
    'aria-labelledby="delete-title" aria-describedby="delete-description" aria-busy="${this._deleting ? "true" : "false"}"',
    'aria-labelledby="discard-title" aria-describedby="discard-description"',
    'aria-labelledby="action-sheet-title" aria-describedby="action-sheet-description"',
    'id="vehicle-form-title"',
    'id="vehicle-form-description"',
    'id="delete-title"',
    'id="delete-description"',
    'id="discard-title"',
    'id="discard-description"',
    'id="action-sheet-title"',
    'id="action-sheet-description"',
    'id="confirm-delete" aria-busy="${this._deleting ? "true" : "false"}"',
    '<button type="button" class="action" id="save-update"',
    '<button type="button" class="action" id="save-create"',
    '<button type="button" class="ghost" id="back-to-list"',
]:
    assert needle in panel, f"Missing retained dialog/accessibility marker: {needle}"

# Accepted fixpoints remain untouched.
assert 'class="form-card preview-card"' in panel
assert 'class="form-card form-section side-season-card' in panel
assert panel.index('class="form-card preview-card"') < panel.index('class="form-card form-section side-season-card')
assert 'class="plate-text-slot"' in panel
assert 'data-renderer-state="text"' in panel
assert 'X/X Treffer' not in panel
assert 'Filter zurücksetzen' not in panel
assert 'Card-Erkennung' in doc

print("r111/r112 Sidebar dialog accessibility cleanup guard OK")
