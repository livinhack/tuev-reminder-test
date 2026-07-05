#!/usr/bin/env python3
"""Validate r070 Sidebar season range parity with backend rules."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert manifest["version"] == "0.1.0-r105"
assert read("REMINDER_VERSION.txt").strip() == "r105"

js = read("custom_components/tuev_reminder/frontend/tuev-reminder-panel.js")
manager = read("custom_components/tuev_reminder/manager.py")

required_js = [
    "_seasonDuration(startMonth, endMonth)",
    "_isValidSeasonRange(startMonth, endMonth)",
    "duration >= 2 && duration <= 11",
    "Saisonzeitraum muss mindestens 2 und höchstens 11 Monate umfassen.",
    "else if (!this._isValidSeasonRange(start, end))",
]
for marker in required_js:
    assert marker in js, marker

required_backend = [
    "def _season_duration(start_month: int, end_month: int) -> int:",
    "return (end_month - start_month) % 12 + 1",
    "2 <= duration <= 11",
    'errors[CONF_SEASON_END_MONTH] = "invalid_season_range"',
]
for marker in required_backend:
    assert marker in manager, marker

print("r070 Sidebar season range validation parity check OK")
