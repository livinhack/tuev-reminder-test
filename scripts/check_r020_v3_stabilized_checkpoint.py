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
assert manifest["version"] == "0.1.0-r087"
assert read("REMINDER_VERSION.txt").strip() == "r087"

init = read("custom_components/tuev_reminder/__init__.py")
calendar = read("custom_components/tuev_reminder/calendar.py")
config_flow = read("custom_components/tuev_reminder/config_flow.py")
readme = read("README.md")
handover = read("HANDOVER.md")
doc = read("docs/REMINDER_R020_V3_STABILIZED_CHECKPOINT.md")

assert_contains(init, 'PLATFORMS = ["sensor"]', "vehicle entries only forward sensor platform")
assert_contains(init, 'discovery.async_load_platform(hass, "calendar", DOMAIN, {}, config)', "integration-level calendar load")
assert_contains(calendar, 'CALENDAR_MANAGER_DEVICE_ID = "calendar_manager"', "detached manager calendar device")
assert_contains(calendar, 'TÜV/HU Erinnerung', "reminder event")
assert_contains(calendar, 'TÜV/HU fällig', "due event")
assert_contains(config_flow, "CONF_REMINDER_OFFSET_DAYS", "offset option")
assert_not_contains(config_flow, "CALENDAR_EVENT_MODE_OPTIONS", "removed calendar mode selector")
assert_not_contains(calendar, "local_calendar", "no local calendar sync")

for text, label in [(readme, "README"), (handover, "HANDOVER"), (doc, "r020 checkpoint doc")]:
    assert_contains(text, "Card b355", label)
    assert_contains(text, "Reminder r020", label)
    assert_contains(text, "calendar.tuev_reminder", label)
    assert_contains(text, "reminder_offset_days", label)

print("r020 v3 stabilized checkpoint check OK")
