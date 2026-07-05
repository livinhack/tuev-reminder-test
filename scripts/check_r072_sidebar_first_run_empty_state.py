#!/usr/bin/env python3
"""Validate r073 Sidebar first-run empty-state polish."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert manifest["version"] == "0.1.0-r087"
assert read("REMINDER_VERSION.txt").strip() == "r087"

panel = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")
assert "Noch keine Fahrzeuge" in panel
assert "first-run-state" in panel
assert "empty-create" in panel
assert 'data-create-trigger="empty"' in panel
assert "Lege dein erstes Fahrzeug an" in panel
assert "Keine Treffer" in panel
assert "Suche leeren" in panel
assert 'id="clear-empty-search"' in panel
assert "filter-empty-state" in panel

readme = read("README.md")
handover = read("HANDOVER.md")
doc = read("docs/REMINDER_R072_SIDEBAR_FIRST_RUN_EMPTY_STATE.md")
compat = read("docs/COMPAT_CARD_B355_REMINDER_R072.md")

assert "Reminder r087" in readme
assert "Sidebar Empty/Search State Polish" in handover
assert "Noch keine Fahrzeuge" in doc
assert "Card remains a separate" in compat

print("r072 Sidebar first-run empty-state check OK")
