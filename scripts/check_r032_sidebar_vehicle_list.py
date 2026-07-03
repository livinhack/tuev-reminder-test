#!/usr/bin/env python3
"""Validate r032 Sidebar read-only vehicle list."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise SystemExit(f"r032 sidebar vehicle list check failed: {message}")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
if manifest.get("version") != "0.1.0-r037":
    fail("manifest version must be 0.1.0-r037")
if read("REMINDER_VERSION.txt").strip() != "r037":
    fail("REMINDER_VERSION.txt must be r032")

panel_py = read("custom_components/tuev_reminder/panel.py")
panel_js = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")

for marker in [
    '"mode": "vehicle_list_polished"',
    '"write_api": False',
]:
    if marker not in panel_py:
        fail(f"panel.py missing marker: {marker}")

for marker in [
    "_filter",
    "_statusFilter",
    "_sort",
    "_visibleVehicles()",
    "manager-table",
    "status-filter",
    "HU-Datum",
    "Status",
    "Name",
    "Treffer",
    "fällig/abgelaufen",
    "keine Card-Funktionen",
    "row-menu",
    "type: \"tuev_reminder/manager/vehicles/list\"",
]:
    if marker not in panel_js:
        fail(f"panel JS missing marker: {marker}")

for forbidden in [
    "confirm_passed",
    "set_due_date",
    "tuev-card",
    "custom:tuev-card",
]:
    if forbidden in panel_js:
        fail(f"panel JS must not duplicate Card/action behavior: {forbidden}")

for relative in [
    "docs/REMINDER_R032_SIDEBAR_VEHICLE_LIST.md",
    "docs/COMPAT_CARD_B355_REMINDER_R032.md",
]:
    if not (ROOT / relative).exists():
        fail(f"missing documentation file: {relative}")

print("r032 sidebar vehicle list check OK")
