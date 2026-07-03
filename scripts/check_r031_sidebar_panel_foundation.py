#!/usr/bin/env python3
"""Validate r031 Sidebar panel foundation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise SystemExit(f"r031 sidebar panel foundation check failed: {message}")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
if manifest.get("version") != "0.1.0-r040":
    fail("manifest version must be 0.1.0-r040")
if read("REMINDER_VERSION.txt").strip() != "r040":
    fail("REMINDER_VERSION.txt must be r031")

required_dependencies = {"http", "frontend", "panel_custom"}
if not required_dependencies.issubset(set(manifest.get("dependencies", []))):
    fail("manifest must declare http, frontend and panel_custom dependencies")

init_py = read("custom_components/tuev_reminder/__init__.py")
panel_py = read("custom_components/tuev_reminder/panel.py")
manager_py = read("custom_components/tuev_reminder/manager.py")
panel_js = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")

for marker in [
    "from .panel import async_register_manager_panel",
    "MANAGER_PANEL_REGISTERED_KEY",
    "await async_register_manager_panel(hass)",
]:
    if marker not in init_py:
        fail(f"__init__.py missing panel registration marker: {marker}")

for marker in [
    "async def async_register_manager_panel",
    "StaticPathConfig(",
    "frontend.async_register_built_in_panel(",
    'component_name="custom"',
    'frontend_url_path=PANEL_URL_PATH',
    '"module_url": PANEL_JS_URL',
    '"write_api": True',
]:
    if marker not in panel_py:
        fail(f"panel.py missing marker: {marker}")

for marker in [
    "customElements.define(\"tuev-reminder-panel\"",
    'type: "tuev_reminder/manager/metadata"',
    'type: "tuev_reminder/manager/vehicles/list"',
    "row-menu",
    "keine Card-Funktionen",
    "hass-toggle-menu",
]:
    if marker not in panel_js:
        fail(f"panel JS missing marker: {marker}")

if '"manager_panel_ready": True' not in manager_py:
    fail("manager metadata must mark manager_panel_ready as true")

for relative in [
    "docs/REMINDER_R031_SIDEBAR_PANEL_FOUNDATION.md",
    "docs/COMPAT_CARD_B355_REMINDER_R031.md",
]:
    if not (ROOT / relative).exists():
        fail(f"missing documentation file: {relative}")

print("r031 sidebar panel foundation check OK")
