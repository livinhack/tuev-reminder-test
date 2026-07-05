#!/usr/bin/env python3
"""Validate retained Sidebar filter empty-state polish."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert manifest["version"] == "0.1.0-r087"
assert read("REMINDER_VERSION.txt").strip() == "r087"

panel = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")
assert "_filtersActive()" in panel
assert "_resetListFilters()" in panel
assert "this._filter = \"\";" in panel
assert "this._statusFilter = \"all\";" in panel
assert "Keine Treffer" in panel
assert "Suche leeren" in panel
assert 'id="clear-empty-search"' in panel
assert 'placeholder="Suchen"' in panel
assert 'placeholder="Search"' not in panel
assert "clear-empty-search" in panel
assert "this._clearSearchFilter()" in panel
assert "state-card" in panel

readme = read("README.md")
handover = read("HANDOVER.md")
doc = read("docs/REMINDER_R071_SIDEBAR_FILTER_EMPTY_STATE.md")
compat = read("docs/COMPAT_CARD_B355_REMINDER_R071.md")

assert "Reminder r087" in readme
assert "Suche leeren" in handover
assert "Filter zurücksetzen" in doc
assert "Card remains a separate" in compat

print("retained Sidebar filter empty-state polish check OK")
