#!/usr/bin/env python3
"""Validate r112 save/error focus hardening in the Sidebar form."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components/tuev_reminder/frontend/tuev-reminder-panel.js"
MANIFEST = ROOT / "custom_components/tuev_reminder/manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"

panel = PANEL.read_text(encoding="utf-8")
manifest = MANIFEST.read_text(encoding="utf-8")
version = VERSION.read_text(encoding="utf-8").strip()

assert '"version": "0.1.0-r114"' in manifest
assert version == "r114"
assert "save validation focuses first blocking issue and backend errors clear stale saving text" in panel
assert "_focusFirstValidationIssue(errors);" in panel
assert "_focusValidationSummary()" in panel
assert 'data-validation-summary tabindex="-1"' in panel
assert ".validation:focus-visible" in panel
assert 'this._formInfo = null;\n      this._formError = err?.message || String(err);\n      this._validationFocusPending = "summary";' in panel
assert 'if (this._validationFocusPending === "summary")' in panel
