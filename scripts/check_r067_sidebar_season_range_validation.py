#!/usr/bin/env python3
"""Validate r070 Sidebar season range parity with backend rules."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert manifest["version"] == "0.1.0-r116"
assert read("REMINDER_VERSION.txt").strip() == "r116"

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

# r116: season helpers live in helpers.py; manager keeps the validation call.
helpers_py = (ROOT / "custom_components/tuev_reminder/helpers.py").read_text(encoding="utf-8")
for marker in [
    "def season_duration(start_month: int, end_month: int) -> int:",
    "return (end_month - start_month) % 12 + 1",
    "2 <= duration <= 11",
]:
    assert marker in helpers_py, marker
for marker in [
    "_is_valid_season_range(start_month, end_month)",
    'errors[CONF_SEASON_END_MONTH] = "invalid_season_range"',
]:
    assert marker in manager, marker

print("r070 Sidebar season range validation parity check OK")
