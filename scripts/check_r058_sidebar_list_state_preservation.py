#!/usr/bin/env python3
"""Validate r058 Sidebar list state preservation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "custom_components" / "tuev_reminder" / "manifest.json"
VERSION = ROOT / "REMINDER_VERSION.txt"
PANEL = ROOT / "custom_components" / "tuev_reminder" / "frontend" / "tuev-reminder-panel.js"
DOC = ROOT / "docs" / "REMINDER_R058_SIDEBAR_LIST_STATE_PRESERVATION.md"
COMPAT = ROOT / "docs" / "COMPAT_CARD_B355_REMINDER_R058.md"


def fail(message: str) -> None:
    raise SystemExit(f"r058 sidebar list state preservation check failed: {message}")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail(f"missing {label}: {needle!r}")


manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("version") != "0.1.0-r098":
    fail("manifest version must be 0.1.0-r098")
if VERSION.read_text(encoding="utf-8").strip() != "r098":
    fail("REMINDER_VERSION.txt must be r058")

panel = PANEL.read_text(encoding="utf-8")
for needle, label in [
    ("_captureListUiState()", "capture helper"),
    ("_restoreListUiState(state = {})", "restore helper"),
    ("_renderPreservingListUiState()", "preserving render helper"),
    ("listScrollLeft", "horizontal scroll preservation"),
    ("selectionStart", "caret preservation"),
    ("this._cssEscape", "selector escaping fallback"),
    ("this._filter = event.target.value", "search input handler"),
    ('this._statusFilter = button.dataset.statusChip || "all"', "status chip filter handler"),
]:
    require(panel, needle, label)

if panel.count("this._renderPreservingListUiState();") < 5:
    fail("expected multiple list interactions to use the preserving render path")

for forbidden in [
    "this._filter = event.target.value;\n        this._openMenuIndex = null;\n        this._openMenuEntryId = null;\n        this._render();",
    "this._statusFilter = event.target.value;\n        this._openMenuIndex = null;\n        this._openMenuEntryId = null;\n        this._render();",
]:
    if forbidden in panel:
        fail("list control still performs a raw full render")

doc = DOC.read_text(encoding="utf-8")
require(doc, "Search input changes now keep focus/caret", "r058 focus documentation")
require(doc, "No Card code", "Reminder/Card separation documentation")
compat = COMPAT.read_text(encoding="utf-8")
require(compat, "Card bridge fields", "compat note must mention unchanged Card bridge")
require(compat, "separate project", "compat note must preserve repo separation")

print("r058 sidebar list state preservation checks passed")
