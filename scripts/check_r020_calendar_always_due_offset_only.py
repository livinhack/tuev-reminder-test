from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

def assert_contains(text: str, needle: str, label: str):
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")

def assert_not_contains(text: str, needle: str, label: str):
    if needle in text:
        raise AssertionError(f"Unexpected {label}: {needle}")

manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert manifest["version"] == "0.1.0-r097"
assert read("REMINDER_VERSION.txt").strip() == "r097"

config_flow = read("custom_components/tuev_reminder/config_flow.py")
calendar = read("custom_components/tuev_reminder/calendar.py")
sensor = read("custom_components/tuev_reminder/sensor.py")
strings = read("custom_components/tuev_reminder/strings.json")
doc = read("docs/REMINDER_R020_CALENDAR_ALWAYS_DUE_OFFSET_ONLY.md")
readme = read("README.md")
handover = read("HANDOVER.md")

assert_not_contains(config_flow, "CALENDAR_EVENT_MODE_OPTIONS", "user-facing calendar event mode options")
assert_not_contains(strings, "calendar_event_mode", "calendar event mode translation field")
assert_contains(config_flow, "CONF_REMINDER_OFFSET_DAYS", "offset field still present")
assert_contains(config_flow, "CALENDAR_EVENT_MODE_REMINDER_AND_DUE", "legacy mode fixed on save")
assert_not_contains(calendar, "_calendar_event_mode", "calendar mode runtime logic")
assert_contains(calendar, "TÜV/HU Erinnerung", "reminder event always present")
assert_contains(calendar, "TÜV/HU fällig", "due event always present")
assert_contains(sensor, "return CALENDAR_EVENT_MODE_REMINDER_AND_DUE", "fixed compatibility sensor mode")
for text, label in [(doc, "r020 doc"), (readme, "README"), (handover, "handover")]:
    assert_contains(text, "reminder_offset_days", label)
    assert_contains(text, "TÜV/HU Erinnerung", label)
    assert_contains(text, "TÜV/HU fällig", label)

print("r020 calendar always-due offset-only check OK")
