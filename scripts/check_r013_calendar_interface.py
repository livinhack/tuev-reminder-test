from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert manifest["version"] == "0.1.0-r014"
assert read("REMINDER_VERSION.txt").strip() == "r014"

const = read("custom_components/tuev_reminder/const.py")
helpers = read("custom_components/tuev_reminder/helpers.py")
config_flow = read("custom_components/tuev_reminder/config_flow.py")
sensor = read("custom_components/tuev_reminder/sensor.py")
calendar = read("custom_components/tuev_reminder/calendar.py")
strings = read("custom_components/tuev_reminder/strings.json")
readme = read("README.md")
handover = read("HANDOVER.md")
doc = read("docs/REMINDER_R013_CALENDAR_EVENT_MODE_OFFSET.md")

for needle in [
    'CONF_CALENDAR_EVENT_MODE = "calendar_event_mode"',
    'CONF_REMINDER_OFFSET_DAYS = "reminder_offset_days"',
    'CALENDAR_EVENT_MODE_REMINDER_ONLY = "reminder_only"',
    'CALENDAR_EVENT_MODE_DUE_ONLY = "due_only"',
    'CALENDAR_EVENT_MODE_REMINDER_AND_DUE = "reminder_and_due"',
    'DEFAULT_REMINDER_OFFSET_DAYS = 7',
]:
    assert_contains(const, needle, "calendar constant")

assert_contains(helpers, "def get_reminder_date(year: int, month: int, offset_days: int = 7)", "offset helper")
assert_contains(helpers, "reminder_offset_days: int = 7", "status offset parameter")
assert_contains(config_flow, "CALENDAR_EVENT_MODE_OPTIONS", "calendar mode selector options")
assert_contains(config_flow, "CONF_CALENDAR_EVENT_MODE", "calendar mode in flow")
assert_contains(config_flow, "CONF_REMINDER_OFFSET_DAYS", "reminder offset in flow")
assert_contains(config_flow, "min=0", "offset minimum")
assert_contains(config_flow, "max=365", "offset maximum")
assert_contains(sensor, '"calendar_event_mode": self.calendar_event_mode', "calendar mode sensor attribute")
assert_contains(sensor, '"reminder_offset_days": self.reminder_offset_days', "offset sensor attribute")
assert_contains(sensor, "get_reminder_date(self.year, self.month, self.reminder_offset_days)", "sensor reminder date offset")
assert_contains(calendar, "def _build_events_for_entry", "calendar multi-event builder")
assert_contains(calendar, 'uid=f"{entry.entry_id}-tuev-reminder"', "reminder event UID")
assert_contains(calendar, 'uid=f"{entry.entry_id}-tuev-due"', "due event UID")
assert_contains(calendar, "TÜV/HU Erinnerung", "reminder summary")
assert_contains(calendar, "TÜV/HU fällig", "due summary")
assert_contains(calendar, "CALENDAR_OWNER_KEY", "shared calendar owner preserved")
for text, label in [(strings, "strings"), (readme, "README"), (handover, "handover"), (doc, "r013 doc")]:
    assert_contains(text, "calendar_event_mode", label)
    assert_contains(text, "reminder_offset_days", label)

print("r013 calendar interface compatibility check OK under r014")
