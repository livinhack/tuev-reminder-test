#!/usr/bin/env python3
"""Validate r112 bundled Sidebar cleanup/check stand."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components/tuev_reminder/manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"
README = ROOT / "README.md"
HANDOVER = ROOT / "HANDOVER.md"
DOC = ROOT / "docs/REMINDER_R110_SIDEBAR_BUNDLED_CLEANUP_CHECKS.md"

panel = PANEL.read_text(encoding="utf-8")
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
version = VERSION.read_text(encoding="utf-8").strip()
readme = README.read_text(encoding="utf-8")
handover = HANDOVER.read_text(encoding="utf-8")
doc = DOC.read_text(encoding="utf-8")

assert manifest["version"] == "0.1.0-r114"
assert version == "r114"
for text, label in [(readme, "README"), (handover, "HANDOVER")]:
    assert "Reminder r114" in text or "TÜV Reminder r114" in text, f"Missing r114 marker in {label}"
    assert "Card-Erkennung" in text, f"Missing no Card detection note in {label}"
assert "Sidebar Bundled Cleanup Checks" in doc
assert "Card-Erkennung" in doc

# r114 cleanup markers
assert "r114 is a bundled cleanup/checkpoint before the next feature block" in panel
assert panel.count("this._openMenuIndex = null;") < 20  # duplicate constructor init removed, not global behavior removed
assert 'role="status" aria-live="polite" aria-atomic="true"' in panel
assert 'setAttribute("aria-busy", this._saving ? "true" : "false")' in panel
assert 'id="back-to-list" ${this._saving ? "disabled" : ""}' in panel

# Accepted layout/fallback fixpoints remain intact.
assert 'class="form-card preview-card"' in panel
assert 'class="form-card form-section side-season-card' in panel
assert panel.index('class="form-card preview-card"') < panel.index('class="form-card form-section side-season-card')
assert 'data-plate-render-slot="text"' in panel
assert 'data-renderer-state="text"' in panel
assert 'class="plate-text-slot"' in panel
assert '.plate-render-slot[data-renderer-state="text"] {' in panel
fallback_block = panel.split('.plate-render-slot[data-renderer-state="text"] {', 1)[1].split('}', 1)[0]
for forbidden in ['background: transparent;', 'border-radius: 0;', 'padding: 0;']:
    assert forbidden not in fallback_block, f"r090 plain fallback must not return: {forbidden}"

# List controls remain intentionally minimal.
assert 'id="clear-search"' in panel
assert 'data-status-chip="${this._escape(value)}"' in panel
assert 'data-create-trigger="controls"' in panel
assert 'X/X Treffer' not in panel
assert 'Filter zurücksetzen' not in panel
assert 'id="sort"' not in panel

# Validation/dirty focus features from r102-r109 remain present.
for needle in [
    'aria-invalid="true" data-invalid="true"',
    'section-invalid',
    'class="validation-link"',
    '_bindValidationLinks();',
    '_focusFirstValidationIssue(errors);',
    'data-dirty-state',
    'this._validationFocusPending = "summary"',
]:
    assert needle in panel, f"Missing retained validation/dirty feature: {needle}"

print("r114 Sidebar bundled cleanup/check guard OK")
