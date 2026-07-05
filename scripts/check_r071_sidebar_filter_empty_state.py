#!/usr/bin/env python3
"""Validate retained Sidebar filter empty-state polish."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert manifest["version"] == "0.1.0-r085"
assert read("REMINDER_VERSION.txt").strip() == "r085"

panel = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")
assert "_filtersActive()" in panel
assert "_resetListFilters()" in panel
assert "this._filter = \"\";" in panel
assert "this._statusFilter = \"all\";" in panel
assert "Keine Treffer" in panel
assert "Filter zurücksetzen" in panel
assert 'id="clear-filters"' in panel
assert 'placeholder="Suchen"' in panel
assert 'placeholder="Search"' not in panel
assert '#clear-filters' in panel
assert "this._resetListFilters()" in panel
assert "state-card" in panel

readme = read("README.md")
handover = read("HANDOVER.md")
doc = read("docs/REMINDER_R071_SIDEBAR_FILTER_EMPTY_STATE.md")
compat = read("docs/COMPAT_CARD_B355_REMINDER_R071.md")

assert "Reminder r073" in readme
assert "Filter zurücksetzen" in handover
assert "Filter zurücksetzen" in doc
assert "Card remains a separate" in compat

print("retained Sidebar filter empty-state polish check OK")
