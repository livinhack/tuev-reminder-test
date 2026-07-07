#!/usr/bin/env python3
"""Guard r114 Sidebar dialog return-focus cleanup."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components/tuev_reminder/manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"
DOC = ROOT / "docs/REMINDER_R113_SIDEBAR_DIALOG_RETURN_FOCUS_CLEANUP.md"

panel = PANEL.read_text(encoding="utf-8")
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
version = VERSION.read_text(encoding="utf-8").strip()
doc = DOC.read_text(encoding="utf-8")

assert manifest["version"] == "0.1.0-r114"
assert version == "r114"
assert "Dialog Return Focus Cleanup" in doc

for needle in [
    "r114 is a bundled cleanup/checkpoint before the next feature block",
    "this._dialogReturnFocus = null;",
    "_rememberDialogReturnFocus(fallbackFocus = null)",
    "_restoreDialogReturnFocus()",
    "this._rememberDialogReturnFocus({ createTrigger: \"controls\" });",
    "this._rememberDialogReturnFocus({ menuEntryId: String(vehicle?.entry_id || \"\") });",
    "this._rememberDialogReturnFocus({ menuEntryId: String(vehicle.entry_id || \"\") });",
    "this._restoreDialogReturnFocus();",
    "if (this._view === \"list\") this._restoreDialogReturnFocus();",
    "_dialogFocusableElements(container)",
    "_keepFocusInsideDialog(event, container)",
    "this._bindDialogKeyboard(modalBackdrop, () => this._closeForm())",
    "data-plate-render-slot=\"text\"",
    "data-renderer-state=\"text\"",
    "class=\"form-card preview-card\"",
    "class=\"form-card form-section side-season-card",
]:
    assert needle in panel, f"Missing r114 marker: {needle}"

assert "return payload;\n    return payload;" not in panel
assert panel.index('class="form-card preview-card"') < panel.index('class="form-card form-section side-season-card')
fallback_block = panel.split('.plate-render-slot[data-renderer-state="text"] {', 1)[1].split('}', 1)[0]
for forbidden in ["background: transparent;", "border-radius: 0;", "padding: 0;"]:
    assert forbidden not in fallback_block, f"r090 plain fallback must not return: {forbidden}"
for forbidden in ["Card-Erkennung eingebaut", "Card-Renderer eingebaut", "Filter zurücksetzen", "X/X Treffer"]:
    assert forbidden not in panel, f"Forbidden marker found: {forbidden}"

print("r114 Sidebar dialog return-focus cleanup guard OK")
