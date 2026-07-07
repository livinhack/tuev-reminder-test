#!/usr/bin/env python3
"""Guard r114 bundled cleanup/checkpoint before next feature work."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components/tuev_reminder/manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"

panel = PANEL.read_text(encoding="utf-8")
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
version = VERSION.read_text(encoding="utf-8").strip()

assert manifest["version"] == "0.1.0-r114"
assert version == "r114"
assert "r114 is a bundled cleanup/checkpoint before the next feature block" in panel

# Accepted visual/UI anchors must remain untouched.
for needle in [
    "preview-card",
    "side-season-card",
    "Saisonzeitraum",
    "plate-render-slot",
    "plate-text-slot",
    'data-plate-render-slot="text"',
    'data-renderer-state="text"',
    'class="list-create-control"',
    'data-create-trigger="controls"',
    'data-dirty-state',
    'data-validation-summary',
    '_rememberDialogReturnFocus',
    '_restoreDialogReturnFocus',
    '_keepFocusInsideDialog',
    'data-dialog-surface',
]:
    assert needle in panel, f"Missing r114 checkpoint marker: {needle}"

# Cleanup guards before the next feature block.
for forbidden in [
    "r090-Plain-Fallback",
    "summary-detail",
    "X/X Treffer",
    "list-add-row top",
    "list-add-row bottom",
    'data-create-trigger="top"',
    'data-create-trigger="bottom"',
    'API v${this._escape(apiVersion)} · ${this._escape(writeApi)}',
    "const apiVersion =",
    "const writeApi =",
    "</div>        </div>",
    "return payload;\n    return payload;",
]:
    assert forbidden not in panel, f"Stale r114 cleanup target still present: {forbidden}"

assert '${this._metadata?.write_api === true ? "" : `<div class="topbar-status read-only" aria-live="polite">Nur lesen</div>`}' in panel
print("r114 sidebar cleanup/checkpoint guard OK")
