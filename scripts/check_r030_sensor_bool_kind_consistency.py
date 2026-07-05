#!/usr/bin/env python3
"""Validate r030 sensor boolean/kind derivation consistency."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise SystemExit(f"r030 sensor bool/kind consistency check failed: {message}")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
if manifest.get("version") != "0.1.0-r097":
    fail("manifest version must be 0.1.0-r097")
if read("REMINDER_VERSION.txt").strip() != "r097":
    fail("REMINDER_VERSION.txt must be r030")

sensor = read("custom_components/tuev_reminder/sensor.py")
manager = read("custom_components/tuev_reminder/manager.py")

required_sensor_needles = [
    "if configured in PLATE_KINDS:",
    "if _coerce_bool(self.data.get(CONF_CHANGE_PLATE_ENABLED, False)):",
    "seasonal = _coerce_bool(self.data.get(CONF_SEASONAL, False))",
    "if self.plate_kind in {PLATE_KIND_GREEN, PLATE_KIND_GREEN_SEASONAL}:",
    "if self.plate_kind in {PLATE_KIND_SEASONAL, PLATE_KIND_GREEN_SEASONAL}:",
    "return _coerce_bool(self.data.get(CONF_SEASONAL, False))",
    "self.plate_kind == PLATE_KIND_CHANGE",
]
for needle in required_sensor_needles:
    if needle not in sensor:
        fail(f"sensor.py missing normalized derivation needle: {needle}")

for forbidden in [
    "if configured:\n            return configured",
    "return bool(self.data.get(CONF_SEASONAL, False))",
    "or bool(self.data.get(CONF_CHANGE_PLATE_ENABLED, False))",
]:
    if forbidden in sensor:
        fail(f"sensor.py still contains legacy fragile boolean/kind code: {forbidden}")

for manager_needle in [
    "if configured in PLATE_KINDS:",
    "return _coerce_bool(values.get(CONF_SEASONAL, False))",
    "return (\n        kind == PLATE_KIND_CHANGE",
]:
    if manager_needle not in manager:
        fail(f"manager.py consistency baseline missing: {manager_needle}")

print("r030 sensor bool/kind consistency check OK")
