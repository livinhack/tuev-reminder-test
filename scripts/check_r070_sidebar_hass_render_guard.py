#!/usr/bin/env python3
"""Validate r070 Sidebar hass setter render guard."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert manifest["version"] == "0.1.0-r078"
assert read("REMINDER_VERSION.txt").strip() == "r078"

panel_js = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")
assert "const firstHass = !this._hass;" in panel_js
assert "this._hass = hass;" in panel_js
assert "this._loadOnce();" in panel_js
assert 'this._view === "list"' in panel_js
assert "this._renderPreservingListUiState();" in panel_js
assert "Rebuilding an\n    // open create/edit/delete dialog" in panel_js

panel_py = read("custom_components/tuev_reminder/panel.py")
assert "require_admin=False" in panel_py
assert "require_admin=True" not in panel_py

print("r070 Sidebar hass render guard check OK")
