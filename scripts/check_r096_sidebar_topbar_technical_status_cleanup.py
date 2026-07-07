#!/usr/bin/env python3
"""Validate r096+ topbar technical status cleanup."""
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
assert '${this._metadata?.write_api === true ? "" : `<div class="topbar-status read-only" aria-live="polite">Nur lesen</div>`}' in panel
assert 'API v${this._escape(apiVersion)} · ${this._escape(writeApi)}' not in panel
assert '<div class="version">API v' not in panel
assert '.topbar-status.read-only' in panel
assert 'r090-Plain-Fallback' not in panel
assert 'plate-render-slot' in panel
assert 'data-renderer-state="text"' in panel
assert 'summary-detail' not in panel or 'X/X Treffer' not in panel
print("r096+ sidebar topbar technical status cleanup check OK")
