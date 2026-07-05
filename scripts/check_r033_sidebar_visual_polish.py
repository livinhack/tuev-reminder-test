#!/usr/bin/env python3
"""Validate r053 Switch-Manager-style Sidebar visual polish."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise SystemExit(f"r053 sidebar visual polish check failed: {message}")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
if manifest.get("version") != "0.1.0-r094":
    fail("manifest version must be 0.1.0-r094")
if read("REMINDER_VERSION.txt").strip() != "r094":
    fail("REMINDER_VERSION.txt must be r053")

panel_py = read("custom_components/tuev_reminder/panel.py")
panel_js = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")

for marker in [
    '"mode": "vehicle_list_create_form_save"',
    '"write_api": True',
]:
    if marker not in panel_py:
        fail(f"panel.py missing marker: {marker}")

for marker in [
    "topbar",
    "toolbar",
    "summary-strip",
    "manager-table",
    "col-preview",
    "preview-cell",
    "plate-preview",
    "plate-eu",
    "row-menu",
    "keine Card-Funktionen",
    "type: \"tuev_reminder/manager/vehicles/list\"",
]:
    if marker not in panel_js:
        fail(f"panel JS missing marker: {marker}")

for forbidden in [
    "confirm_passed",
    "set_due_date",
    "custom:tuev-card",
    "import(\"/local",
    "module_url: \"/local",
]:
    if forbidden in panel_js:
        fail(f"panel JS must not duplicate Card/action behavior: {forbidden}")

for relative in [
    "docs/REMINDER_R033_SWITCH_MANAGER_STYLE_POLISH.md",
    "docs/COMPAT_CARD_B355_REMINDER_R033.md",
]:
    if not (ROOT / relative).exists():
        fail(f"missing documentation file: {relative}")

print("r053 sidebar visual polish check OK")
