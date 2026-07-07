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
assert manifest["version"] == "0.1.0-r114"
assert read("REMINDER_VERSION.txt").strip() == "r114"

init = read("custom_components/tuev_reminder/__init__.py")
calendar = read("custom_components/tuev_reminder/calendar.py")
readme = read("README.md")
handover = read("HANDOVER.md")
test_matrix = read("docs/REMINDER_R020_V3_STABILIZATION_TEST_MATRIX.md")
compat = read("docs/COMPAT_CARD_B355_REMINDER_R017.md")
audit = read("docs/REMINDER_R020_RELEASE_READINESS_AUDIT.md")

# r017 runtime boundary must remain intact.
assert_contains(init, 'PLATFORMS = ["sensor"]', "vehicle entries forward sensors only")
assert_contains(init, 'discovery.async_load_platform(hass, "calendar", DOMAIN, {}, config)', "integration-level calendar load")
assert_contains(calendar, 'CALENDAR_MANAGER_DEVICE_ID = "calendar_manager"', "manager calendar device id")
assert_contains(calendar, 'identifiers={(DOMAIN, CALENDAR_MANAGER_DEVICE_ID)}', "manager device info")
assert_contains(calendar, 'for entry in self.hass.config_entries.async_entries(DOMAIN):', "calendar builds from all entries")
assert_not_contains(calendar, 'calendar_owner_entry_id', "old vehicle owner key")
assert_not_contains(calendar, 'async_setup_entry(', "calendar must not be forwarded as vehicle-entry platform")
assert_not_contains(calendar, 'local_calendar', "local calendar sync")
assert_not_contains(calendar, '_calendar_event_mode', "calendar mode branch removed")
assert_contains(calendar, 'uid=f"{entry.entry_id}-tuev-reminder"', "reminder event kept")
assert_contains(calendar, 'uid=f"{entry.entry_id}-tuev-due"', "due event kept")

# r018/r020 docs must cover the stabilization scope.
assert_contains(readme, "TÜV Reminder r020", "README r020")
assert_contains(handover, "Calendar Always Due", "handover title")
assert_contains(test_matrix, "Card b355", "test matrix card baseline")
assert_contains(test_matrix, "Reminder r020", "test matrix reminder baseline")
assert_contains(test_matrix, "Wechselkennzeichen + verkleinert zweizeilig -> rejected", "format validation test")
assert_contains(test_matrix, "calendar.tuev_reminder", "calendar test")
assert_contains(test_matrix, "tuev_reminder.confirm_passed", "service test")
assert_contains(compat, "Card b355 + Reminder r017/r020", "compat title")
assert_contains(audit, "r017:      detached integration-level calendar entity", "release audit r017")
assert_contains(audit, "r020:      stabilization test matrix", "release audit r020")

print("r018/r020 v3 stabilization checkpoint check OK")
