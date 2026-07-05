from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
version = (ROOT / "REMINDER_VERSION.txt").read_text(encoding="utf-8").strip()
if version != "r017":
    print(f"r017 detached calendar entity check skipped for current version {version}")
    raise SystemExit(0)

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

def assert_contains(text: str, needle: str, label: str):
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")

def assert_not_contains(text: str, needle: str, label: str):
    if needle in text:
        raise AssertionError(f"Unexpected {label}: {needle}")

manifest = json.loads(read("custom_components/tuev_reminder/manifest.json"))
assert manifest["version"] == "0.1.0-r017"
assert read("REMINDER_VERSION.txt").strip() == "r066"

init = read("custom_components/tuev_reminder/__init__.py")
calendar = read("custom_components/tuev_reminder/calendar.py")
readme = read("README.md")
handover = read("HANDOVER.md")
doc = read("docs/REMINDER_R017_DETACHED_CALENDAR_ENTITY.md")

assert_contains(init, 'PLATFORMS = ["sensor"]', "vehicle entries forward sensors only")
assert_contains(init, 'discovery.async_load_platform(hass, "calendar", DOMAIN, {}, config)', "integration-level calendar platform load")
assert_contains(init, 'CALENDAR_PLATFORM_LOADED_KEY = "calendar_platform_loaded"', "calendar platform load guard")
assert_contains(calendar, 'async def async_setup_platform(', "calendar platform setup")
assert_contains(calendar, 'CALENDAR_ENTITY_ADDED_KEY = "calendar_entity_added"', "calendar entity added guard")
assert_contains(calendar, 'CALENDAR_MANAGER_DEVICE_ID = "calendar_manager"', "manager device id")
assert_contains(calendar, 'identifiers={(DOMAIN, CALENDAR_MANAGER_DEVICE_ID)}', "manager device info")
assert_contains(calendar, 'for entry in self.hass.config_entries.async_entries(DOMAIN):', "calendar still builds from all vehicle entries")
assert_not_contains(calendar, 'calendar_owner_entry_id', "old vehicle owner key")
assert_not_contains(calendar, 'calendar_loaded_entry_ids', "old loaded vehicle entries key")
assert_not_contains(calendar, 'async_reload(replacement.entry_id)', "old owner handoff reload")
assert_not_contains(calendar, 'async_setup_entry(', "calendar must not be set up as vehicle-entry platform")
assert_not_contains(init, 'PLATFORMS = ["sensor", "calendar"]', "calendar must not be forwarded as a vehicle platform")
assert_contains(doc, "not be semantically owned by one vehicle", "r017 detached calendar doc")
assert_contains(readme, "Reminder r017", "README r017")
assert_contains(handover, "Detached Calendar Entity", "handover title")
assert_not_contains(calendar, "local_calendar", "local calendar write/sync")

print("r017 detached calendar entity check OK")
