#!/usr/bin/env python3
"""Validate the r029 service-entry resolver await fix."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise SystemExit(f"r029 service await fix check failed: {message}")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
if manifest.get("version") != "0.1.0-r043":
    fail("manifest version must be 0.1.0-r043")

if read("REMINDER_VERSION.txt").strip() != "r043":
    fail("REMINDER_VERSION.txt must be r029")

init_py = read("custom_components/tuev_reminder/__init__.py")

if "entry = _resolve_tuev_entry(hass, entity_id)" in init_py:
    fail("service handlers must not call async _resolve_tuev_entry without await")

await_marker = "entry = await _resolve_tuev_entry(hass, entity_id)"
if init_py.count(await_marker) != 2:
    fail("both service handlers must await _resolve_tuev_entry")

for service_marker in [
    "async def handle_confirm_passed(call: ServiceCall):",
    "async def handle_set_due_date(call: ServiceCall):",
    "await _async_store_updated_options(hass, entry, new_options)",
]:
    if service_marker not in init_py:
        fail(f"missing service marker: {service_marker}")

for relative in [
    "docs/REMINDER_R029_SERVICE_AWAIT_FIX.md",
    "docs/COMPAT_CARD_B355_REMINDER_R029.md",
]:
    if not (ROOT / relative).exists():
        fail(f"missing documentation file: {relative}")

print("r029 service await fix OK")
