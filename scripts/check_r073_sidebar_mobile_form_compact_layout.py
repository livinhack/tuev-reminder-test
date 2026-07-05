#!/usr/bin/env python3
"""Validate r073 Sidebar mobile Create/Edit form compact layout."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert manifest["version"] == "0.1.0-r097"
assert read("REMINDER_VERSION.txt").strip() == "r097"

panel = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")
assert 'class="form-shell vehicle-form-shell"' in panel
assert '@media (max-width: 720px)' in panel
assert '.vehicle-form-shell {' in panel
assert 'min-height: 100vh;' in panel
assert 'padding: 12px 12px 88px;' in panel
assert 'font-size: 16px;' in panel
assert 'env(safe-area-inset-bottom)' in panel
assert '.vehicle-form-shell .modal-bottom-actions' in panel
assert 'position: fixed;' in panel
assert 'width: 100%;' in panel
assert 'max-width: 100%;' in panel
assert '.vehicle-form-shell .note' in panel
assert 'display: none;' in panel

readme = read("README.md")
handover = read("HANDOVER.md")
doc = read("docs/REMINDER_R073_SIDEBAR_MOBILE_FORM_COMPACT_LAYOUT.md")
compat = read("docs/COMPAT_CARD_B355_REMINDER_R073.md")

assert "Reminder r073" in readme
assert "Sidebar Mobile Form Compact Layout" in handover
assert "fixed bottom action bar" in doc
assert "Card remains a separate" in compat

print("r073 Sidebar mobile form compact layout check OK")
