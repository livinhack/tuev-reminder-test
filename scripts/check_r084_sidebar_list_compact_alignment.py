#!/usr/bin/env python3
"""Validate r085 Sidebar compact list alignment."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"


def fail(message: str) -> None:
    raise SystemExit(message)

manifest = json.loads((ROOT / "custom_components" / "tuev_reminder" / "manifest.json").read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r087":
    fail("manifest version must be 0.1.0-r087")
if (ROOT / "REMINDER_VERSION.txt").read_text(encoding="utf-8").strip() != "r087":
    fail("REMINDER_VERSION must be r085")

panel = PANEL.read_text(encoding="utf-8")
required = [
    "th, td { padding: 8px 12px;",
    ".vehicle-title { font-weight: 600; line-height: 1.2; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }",
    "padding: 7px 6px;",
    "padding: 10px 56px 6px 12px;",
    "grid-template-columns: 82px minmax(0, 1fr);",
    ".mobile-plate-text { display: block; font-size: 11px; margin-top: 2px; }",
]
for needle in required:
    if needle not in panel:
        fail(f"missing r085 compact layout marker: {needle}")

for forbidden in [
    "vehicle-meta-line",
    "class=\"tag\"",
    ".tag-row",
    "row-status-",
    "status-text-",
    "border-left: 4px solid",
]:
    if forbidden in panel:
        fail(f"obsolete duplicated list information came back: {forbidden}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
handover = (ROOT / "HANDOVER.md").read_text(encoding="utf-8")
changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
for needle in ["Reminder r085", "compact", "meta/tag line"]:
    if needle not in readme:
        fail(f"README missing r085 note: {needle}")
if "Sidebar List Compact Alignment" not in handover:
    fail("HANDOVER must describe r085 compact alignment")
if not (ROOT / "docs" / "COMPAT_CARD_B355_REMINDER_R085.md").exists():
    fail("r085 compatibility file missing")

print("r085 Sidebar compact list alignment checks passed")
